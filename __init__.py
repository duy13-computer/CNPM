from infrastructure.databases.mssql import init_mssql
from infrastructure.models import admin_model, appraiser_model, appraisals_model, buyer_model, feedback_model, payment_model, seller_model, transaction_model, user_model, watch_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base