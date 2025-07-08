from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
from app.models import (
    get_db, Match, Question, Response, User, Analysis, Base, engine
)
from app.utils.youtube import download_youtube_audio
from app.utils.whisper_transcribe import transcribe_audio
from app.utils.gpt4o import generate_yesno_questions, generate_analysis
import sqlalchemy.exc

blp = Blueprint("Engagement", "football_engagement", url_prefix="/api", description="Core engagement endpoints")

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# PUBLIC_INTERFACE
@blp.route("/ingest", methods=["POST"])
class IngestMatch(MethodView):
    """
    Ingest a new match from a YouTube URL, extract audio, transcribe, and generate questions.
    Request: { "youtube_url": "https://youtube.com/..." }
    Response: { "match_id": ..., "questions": [...] }
    """
    def post(self):
        data = request.get_json()
        url = data.get("youtube_url")
        if not url:
            abort(400, message="youtube_url required")
        db = next(get_db())

        try:
            match = Match(youtube_url=url, status="processing")
            db.add(match)
            db.commit()
            db.refresh(match)
        except sqlalchemy.exc.SQLAlchemyError:
            abort(500, message="Failed to add match to database.")

        try:
            audio_path = download_youtube_audio(url)
            transcript = transcribe_audio(audio_path)
            questions = generate_yesno_questions(transcript, num_questions=3)
            # Store questions
            question_objs = []
            for q in questions:
                qobj = Question(match_id=match.id, question_text=q)
                db.add(qobj)
                db.commit()
                db.refresh(qobj)
                question_objs.append(qobj)
            match.status = "ready"
            db.commit()
            return {
                "match_id": match.id,
                "questions": [q.question_text for q in question_objs],
            }
        except Exception as e:
            match.status = "error"
            db.commit()
            abort(500, message=f"Ingest failed: {e}")

# PUBLIC_INTERFACE
@blp.route("/matches/<int:match_id>/questions", methods=["GET"])
class GetQuestions(MethodView):
    """Get questions for a match."""
    def get(self, match_id):
        db = next(get_db())
        questions = db.query(Question).filter(Question.match_id==match_id).all()
        return {"questions": [ {"question_id":q.id, "text":q.question_text} for q in questions ]}

# PUBLIC_INTERFACE
@blp.route("/questions/<int:question_id>/answer", methods=["POST"])
class AnswerQuestion(MethodView):
    """
    Submit an answer for a yes/no question.
    Request: { "username": "alice", "answer": true }
    """
    def post(self, question_id):
        data = request.get_json()
        username = data.get("username")
        answer = data.get("answer")  # true/false

        if username is None or answer is None:
            abort(400, message="username and answer required")
        db = next(get_db())
        # Find or create user
        user = db.query(User).filter(User.username==username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)
        response = Response(user_id=user.id, question_id=question_id, answer=bool(answer))
        db.add(response)
        db.commit()
        return {"message": "Answer recorded."}

# PUBLIC_INTERFACE
@blp.route("/questions/<int:question_id>/analytics", methods=["GET"])
class AnalyticsQuestion(MethodView):
    """
    Get analytics (yes/no counts + analysis) for a question.
    Response: { "yes": int, "no": int, "analysis": str }
    """
    def get(self, question_id):
        db = next(get_db())
        responses = db.query(Response).filter(Response.question_id==question_id).all()
        yes = sum(1 for r in responses if r.answer)
        no = sum(1 for r in responses if not r.answer)
        # Fetch question
        question = db.query(Question).filter(Question.id==question_id).first()
        if not question:
            abort(404, message="Question not found.")
        # Analysis: check cache or regenerate
        existing = db.query(Analysis).filter(Analysis.question_id==question_id).first()
        if not existing:
            try:
                text = generate_analysis(question.question_text, {'yes':yes,'no':no})
            except Exception:
                text = "Analysis unavailable."
            existing = Analysis(question_id=question_id, analysis_text=text)
            db.add(existing)
            db.commit()
        return {"yes": yes, "no": no, "analysis": existing.analysis_text}
