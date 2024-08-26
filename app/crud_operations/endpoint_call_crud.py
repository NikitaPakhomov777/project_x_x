from sqlalchemy.orm import Session
from app.models.endpoint_call import EndpointCall


class EndpointCallCrud:

    @staticmethod
    def increment_call_count(session: Session, endpoint_name: str):
        endpoint_call = session.query(EndpointCall).filter_by(endpoint_name=endpoint_name).first()
        if not endpoint_call:
            endpoint_call = EndpointCall(endpoint_name=endpoint_name, call_count=1)
            session.add(endpoint_call)
        else:
            endpoint_call.call_count += 1
        session.commit()
        session.refresh(endpoint_call)

    @classmethod
    def get_calls_endpoints_count(cls, skip, limit, session):
        get_calls_count = session.query(EndpointCall).order_by(EndpointCall.id).offset(skip).limit(limit).all()
        return get_calls_count
