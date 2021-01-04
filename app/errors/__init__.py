from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
"""
Blueprint類獲取 blueprint 的名稱，
基礎模組的名稱（通常在 Flask 應用例項中設定為__name__）
以及一些可選引數（在這種情況下我不需要這些引數）。 
Blueprint 物件建立後，我匯入了handlers.py模組，
以便其中的錯誤處理程式在 blueprint 中註冊。 
該匯入位於底部以避免迴圈依賴。
"""