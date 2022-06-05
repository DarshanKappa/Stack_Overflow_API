import re
from Q_and_A.models import Answers, Questions
from pydantic import BaseModel, validator, ValidationError
from django.contrib.auth.models import User


class QuestionValidation(BaseModel):
    title: str
    body: str
    tag: str
    
    @validator("title", pre=False)
    def check_title(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v

    @validator("body", pre=False)
    def check_body(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v

    @validator("tag", pre=False)
    def check_tag(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v
    
    class Config:
        extra = 'forbid'
        
class AnswerValidation(BaseModel):
    question: int
    body: str
    
    @validator("body", pre=False)
    def check_body(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v
    
    @validator("question", pre=False)
    def check_question(cls, v):
        if not Questions.objects.filter(pk=int(v)).first():
            raise ValueError("Invalid question id")
        return v
    
    class Config:
        extra = 'forbid'


class AnswerApprovalVlaidation(BaseModel):
    answer_id: int
    
    @validator('answer_id')
    def check_answer_id(cls, v):
        if not Answers.objects.filter(pk=int(v)).first():
            raise ValueError("Invalid answer id")
        return v
    
    class Config:
        extra = 'forbid'