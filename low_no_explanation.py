import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os
import re
import math
from openai import OpenAI
from streamlit_image_coordinates import streamlit_image_coordinates
from fabric_texture import apply_fabric_texture
from svg_utils import convert_svg_to_png

# API配置信息
API_KEY = "sk-lNVAREVHjj386FDCd9McOL7k66DZCUkTp6IbV0u9970qqdlg"
BASE_URL = "https://api.deepbricks.ai/v1/"

def show_low_complexity_general_sales():
    st.title("👕 AI Co-Creation Experiment Platform")
    st.markdown("### Low Task Complexity-General Sales - Create Your Unique T-shirt Design")
    
    # 初始化T恤颜色和纹理状态变量
    if 'shirt_color_hex' not in st.session_state:
        st.session_state.shirt_color_hex = "#FFFFFF"  # 默认白色
    if 'current_applied_color' not in st.session_state:
        st.session_state.current_applied_color = st.session_state.shirt_color_hex
    if 'current_applied_fabric' not in st.session_state:
        st.session_state.current_applied_fabric = None
    if 'original_base_image' not in st.session_state:
        st.session_state.original_base_image = None
    if 'base_image' not in st.session_state:
        st.session_state.base_image = None
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'final_design' not in st.session_state:
        st.session_state.final_design = None
    if 'ai_suggestions' not in st.session_state:
        st.session_state.ai_suggestions = None
    
    # 创建左右两列布局
    preview_col, controls_col = st.columns([3, 2])
    
    with preview_col:
        st.markdown("### T-shirt Design")
        if st.session_state.base_image is None:
            try:
                # 加载原始白色T恤图像
                original_image_path = "white_shirt.png"
                if os.path.exists(original_image_path):
                    original_image = Image.open(original_image_path).convert("RGBA")
                    st.session_state.original_base_image = original_image.copy()
                    st.session_state.base_image = original_image.copy()
                    st.session_state.current_image = original_image.copy()
                    st.session_state.final_design = original_image.copy()
                    st.session_state.logo_auto_generated = False
                    st.session_state.show_generated_logo = False
                    st.session_state.applied_logo = None
                    st.session_state.applied_text = None
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                    st.session_state.text_size_info = {"font_size": 39, "text_width": original_image.width, "text_height": original_image.height, "scale_factor": 1.0}
                    st.session_state.font_debug_info = []
                    st.session_state.loaded_font_path = None
                    st.session_state.using_fallback_text = False
                    st.session_state.tshirt_size = original_image.size
                    st.session_state.design_area = (0, 0, original_image.width, original_image.height)
                    st.session_state.text_position = (original_image.width // 2, original_image.height // 3)
                
                # 重置颜色为默认白色
                st.session_state.shirt_color_hex = "#FFFFFF"
                st.session_state.current_applied_color = "#FFFFFF"
                
                # 重置纹理为无
                st.session_state.fabric_type = None
                st.session_state.current_applied_fabric = None
                
                # 直接使用原始T恤图像，不应用任何纹理或颜色
                if st.session_state.original_base_image is not None:
                    # 使用原始白色T恤图像的直接副本
                    original_image = st.session_state.original_base_image.copy()
                    
                    # 更新所有相关图像为原始图像
                    st.session_state.base_image = original_image
                    st.session_state.final_design = original_image.copy()
                    
                    # 重置当前图像为带选择框的原始图像
                    temp_image, current_pos = draw_selection_box(original_image)
                    st.session_state.current_image = temp_image
                    st.session_state.current_box_position = current_pos
                    
                    print("已重置为原始T恤图像，没有应用任何纹理")
                else:
                    print("无法重置设计：原始图像不存在")
                
                # 强制刷新界面
                st.success("已清除所有设计并恢复原始T恤")
                st.rerun()
            
            # 下载和确认按钮
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                buf = BytesIO()
                st.session_state.final_design.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label="💾 Download design",
                    data=buf,
                    file_name="custom_tshirt.png",
                    mime="image/png"
                )
            
            with dl_col2:
                # Confirm completion button
                if st.button("Confirm completion"):
                    st.session_state.page = "survey"
                    st.rerun()
    
    with controls_col:
        # 操作区，包含AI建议和其他控制选项
        with st.expander("🤖 AI design suggestions", expanded=True):
            st.markdown("#### Get AI Suggestions")
            # 添加用户偏好输入
            user_preference = st.text_input("Describe your preferred style or usage", placeholder="For example: sports style, business场合, casual daily, etc.")
            
            # 添加获取建议按钮
            if st.button("Get personalized AI suggestions", key="get_ai_advice"):
                with st.spinner("Generating personalized design suggestions..."):
                    suggestions = get_ai_design_suggestions(
                        user_preferences=user_preference
                    )
                    st.session_state.ai_suggestions = suggestions
                    st.success("AI suggestions have been applied to your design options!")

        # 将应用建议的部分移出条件判断，确保始终显示
        with st.expander("🎨 Color & Fabric", expanded=True):
            st.markdown("#### T-shirt Color")
            
            # 颜色建议应用
            if 'ai_suggested_colors' not in st.session_state:
                # 初始提供一些默认颜色选项
                st.session_state.ai_suggested_colors = {
                    "white": "#FFFFFF", 
                    "black": "#000000", 
                    "navy blue": "#003366", 
                    "light gray": "#CCCCCC", 
                    "light blue": "#ADD8E6"
                }
            
            # 创建颜色选择列表 - 动态创建
            colors = st.session_state.ai_suggested_colors
            color_cols = st.columns(min(3, len(colors)))
            
            for i, (color_name, color_hex) in enumerate(colors.items()):
                with color_cols[i % 3]:
                    # 显示颜色预览
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {color_hex}; 
                            width: 100%; 
                            height: 40px; 
                            border-radius: 5px;
                            border: 1px solid #ddd;
                            margin-bottom: 5px;">
                        </div>
                        <div style="text-align: center; margin-bottom: 10px;">
                            {color_name}<br>
                            <span style="font-family: monospace; font-size: 0.9em;">{color_hex}</span>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    if st.button(f"Apply {color_name}", key=f"apply_{i}"):
                        st.session_state.shirt_color_hex = color_hex
                        st.rerun()
            
            # 添加自定义颜色调整功能
            st.markdown("##### Custom color")
            custom_color = st.color_picker("Select a custom color:", st.session_state.shirt_color_hex, key="custom_color_picker")
            custom_col1, custom_col2 = st.columns([3, 1])
            
            with custom_col1:
                # 显示自定义颜色预览
                st.markdown(
                    f"""
                    <div style="
                        background-color: {custom_color}; 
                        width: 100%; 
                        height: 40px; 
                        border-radius: 5px;
                        border: 1px solid #ddd;
                        margin-bottom: 5px;">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            with custom_col2:
                if st.button("Apply custom color"):
                    st.session_state.shirt_color_hex = custom_color
                    st.rerun()
            
            # 添加面料纹理选择
            st.markdown("#### Fabric Texture")
            if 'fabric_type' not in st.session_state:
                st.session_state.fabric_type = "Cotton"  # 默认面料类型
            
            # 面料选择
            fabric_options = ["Cotton", "Polyester", "Cotton-Polyester Blend", "Jersey", "Linen", "Bamboo"]
            fabric_type = st.selectbox("Fabric type:", fabric_options,
                                    index=fabric_options.index(st.session_state.fabric_type)
                                    if st.session_state.fabric_type in fabric_options else 0)
            
            # 应用面料纹理按钮
            if st.button("Apply Texture"):
                # 更新存储的面料值
                old_fabric = st.session_state.fabric_type
                st.session_state.fabric_type = fabric_type
                
                # 无论面料类型是否改变，都应用纹理
                if st.session_state.original_base_image is not None:
                    try:
                        # 应用纹理
                        new_colored_image = change_shirt_color(
                            st.session_state.original_base_image, 
                            st.session_state.shirt_color_hex,
                            apply_texture=True, 
                            fabric_type=fabric_type
                        )
                        st.session_state.base_image = new_colored_image
                        
                        # 更新当前图像
                        new_image, _ = draw_selection_box(new_colored_image, st.session_state.current_box_position)
                        st.session_state.current_image = new_image
                        
                        # 如果有最终设计，也需要更新
                        if st.session_state.final_design is not None:
                            st.session_state.final_design = new_colored_image.copy()
                        
                        st.rerun()
                    except Exception as e:
                        st.warning(f"应用面料纹理时出错: {e}")
                
                # 显示确认信息
                st.success(f"Fabric texture updated: {fabric_type}")
        
        # 文字设计部分 - 独立出来，确保始终显示
        with st.expander("✍️ Text Design", expanded=True):
            # 显示AI建议的文字候选项
            if 'ai_suggested_texts' in st.session_state and st.session_state.ai_suggested_texts:
                st.markdown("**AI Suggested Text Options:**")
                
                # 创建候选项网格布局
                text_suggestions = st.session_state.ai_suggested_texts
                suggestion_cols = st.columns(min(3, len(text_suggestions)))
                
                for i, suggestion in enumerate(text_suggestions):
                    with suggestion_cols[i % 3]:
                        # 使用Streamlit按钮替代HTML点击事件
                        if st.button(suggestion, key=f"suggestion_{i}"):
                            st.session_state.ai_text_suggestion = suggestion
                            st.rerun()
            
            # 文字选项
            text_col1, text_col2 = st.columns([2, 1])
            
            with text_col1:
                # 使用临时变量的值作为默认值
                default_input = ""
                if 'temp_text_selection' in st.session_state:
                    default_input = st.session_state.temp_text_selection
                    # 使用后清除临时状态
                    del st.session_state.temp_text_selection
                elif 'ai_text_suggestion' in st.session_state:
                    default_input = st.session_state.ai_text_suggestion
                
                text_content = st.text_input("Enter or copy AI recommended text", default_input, key="ai_text_suggestion")
            
            with text_col2:
                text_color = st.color_picker("Text color:", "#000000", key="ai_text_color")
            
            # 字体选择 - 扩展为高复杂度方案的选项
            font_options = ["Arial", "Times New Roman", "Courier", "Verdana", "Georgia", "Script", "Impact"]
            font_family = st.selectbox("Font family:", font_options, key="ai_font_selection")
            
            # 添加文字样式选项
            text_style = st.multiselect("Text style:", ["Bold", "Italic", "Underline", "Shadow", "Outline"], default=["Bold"])
            
            # 添加动态文字大小滑块 - 增加最大值
            text_size = st.slider("Text size:", 20, 400, 39, key="ai_text_size")
            
            # 添加文字效果选项
            text_effect = st.selectbox("Text effect:", ["None", "Bent", "Arch", "Wave", "3D", "Gradient"])
            
            # 添加对齐方式选项
            alignment = st.radio("Alignment:", ["Left", "Center", "Right"], horizontal=True, index=1)
            
            # 修改预览部分，将中文样式转换为英文样式名称
            if text_content:
                # 构建样式字符串
                style_str = ""
                if "Bold" in text_style:
                    style_str += "font-weight: bold; "
                if "Italic" in text_style:
                    style_str += "font-style: italic; "
                if "Underline" in text_style:
                    style_str += "text-decoration: underline; "
                if "Shadow" in text_style:
                    style_str += "text-shadow: 2px 2px 4px rgba(0,0,0,0.5); "
                if "Outline" in text_style:
                    style_str += "-webkit-text-stroke: 1px #000; "
                
                # 处理对齐
                align_str = "center"
                if alignment == "Left":
                    align_str = "left"
                elif alignment == "Right":
                    align_str = "right"
                
                # 处理效果
                effect_str = ""
                if text_effect == "Bent":
                    effect_str = "transform: rotateX(10deg); transform-origin: center; "
                elif text_effect == "Arch":
                    effect_str = "transform: perspective(100px) rotateX(10deg); "
                elif text_effect == "Wave":
                    effect_str = "display: inline-block; transform: translateY(5px); animation: wave 2s ease-in-out infinite; "
                elif text_effect == "3D":
                    effect_str = "text-shadow: 0 1px 0 #ccc, 0 2px 0 #c9c9c9, 0 3px 0 #bbb; "
                elif text_effect == "Gradient":
                    effect_str = "background: linear-gradient(45deg, #f3ec78, #af4261); -webkit-background-clip: text; -webkit-text-fill-color: transparent; "
                
                preview_size = text_size * 1.5  # 预览大小略大
                st.markdown(
                    f"""
                    <style>
                    @keyframes wave {{
                        0%, 100% {{ transform: translateY(0px); }}
                        50% {{ transform: translateY(-10px); }}
                    }}
                    </style>
                    <div style="
                        padding: 10px;
                        margin: 10px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        font-family: {font_family}, sans-serif;
                        color: {text_color};
                        text-align: {align_str};
                        font-size: {preview_size}px;
                        line-height: 1.2;
                        {style_str}
                        {effect_str}
                    ">
                    {text_content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            # 应用文字按钮
            if st.button("Apply text to design", key="apply_ai_text"):
                if not text_content.strip():
                    st.warning("Please enter text content!")
                else:
                    # 文字应用逻辑
                    with st.spinner("Applying text design..."):
                        try:
                            # 获取当前图像
                            if st.session_state.final_design is not None:
                                new_design = st.session_state.final_design.copy()
                            else:
                                new_design = st.session_state.base_image.copy()
                            
                            # 获取图像尺寸
                            img_width, img_height = new_design.size
                            
                            # 添加调试信息
                            st.session_state.tshirt_size = (img_width, img_height)
                            
                            # 创建透明的文本图层，大小与T恤相同
                            text_layer = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
                            text_draw = ImageDraw.Draw(text_layer)
                            
                            # 加载字体
                            from PIL import ImageFont
                            import os
                            import platform
                            
                            # 初始化调试信息列表
                            font_debug_info = []
                            font_debug_info.append("Starting text design application")
                            
                            # 尝试加载系统字体
                            font = None
                            try:
                                # 记录系统信息以便调试
                                system = platform.system()
                                font_debug_info.append(f"System type: {system}")
                                
                                # 根据不同系统尝试不同的字体路径
                                if system == 'Windows':
                                    # Windows系统字体路径
                                    font_paths = [
                                        "C:/Windows/Fonts/arial.ttf",
                                        "C:/Windows/Fonts/ARIAL.TTF",
                                        "C:/Windows/Fonts/calibri.ttf",
                                        "C:/Windows/Fonts/simsun.ttc",  # 中文宋体
                                        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                                    ]
                                elif system == 'Darwin':  # macOS
                                    font_paths = [
                                        "/Library/Fonts/Arial.ttf",
                                        "/System/Library/Fonts/Helvetica.ttc",
                                        "/System/Library/Fonts/PingFang.ttc"  # 苹方字体
                                    ]
                                else:  # Linux或其他
                                    font_paths = [
                                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
                                        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
                                    ]
                                
                                # 设定字体大小
                                render_size = text_size
                                font_debug_info.append(f"Trying to load font, size: {render_size}px")
                                
                                # 尝试加载每个字体
                                for font_path in font_paths:
                                    if os.path.exists(font_path):
                                        try:
                                            font = ImageFont.truetype(font_path, render_size)
                                            st.session_state.loaded_font_path = font_path
                                            font_debug_info.append(f"Successfully loaded font: {font_path}")
                                            break
                                        except Exception as font_err:
                                            font_debug_info.append(f"Load font failed: {font_path} - {str(font_err)}")
                            except Exception as e:
                                font_debug_info.append(f"Font loading process error: {str(e)}")
                            
                            # 如果系统字体加载失败，使用默认字体
                            if font is None:
                                try:
                                    font_debug_info.append("Using PIL default font")
                                    font = ImageFont.load_default()
                                    st.session_state.using_fallback_text = True
                                except Exception as default_err:
                                    font_debug_info.append(f"Default font loading failed: {str(default_err)}")
                            
                            # 文本渲染逻辑
                            if font:
                                # 处理文本换行 - 当文本太长时
                                max_text_width = int(img_width * 0.7)  # 最大文本宽度为T恤宽度的70%
                                lines = []
                                words = text_content.split()
                                current_line = words[0] if words else ""
                                
                                # 逐词检查并换行
                                for word in words[1:]:
                                    test_line = current_line + " " + word
                                    # 检查添加这个词后的宽度
                                    test_bbox = text_draw.textbbox((0, 0), test_line, font=font)
                                    test_width = test_bbox[2] - test_bbox[0]
                                    
                                    if test_width <= max_text_width:
                                        current_line = test_line
                                    else:
                                        lines.append(current_line)
                                        current_line = word
                                
                                # 添加最后一行
                                lines.append(current_line)
                                
                                # 计算总高度和最大宽度
                                line_height = render_size * 1.2  # 行高略大于字体大小
                                total_height = len(lines) * line_height
                                max_width = 0
                                
                                for line in lines:
                                    line_bbox = text_draw.textbbox((0, 0), line, font=font)
                                    line_width = line_bbox[2] - line_bbox[0]
                                    max_width = max(max_width, line_width)
                                
                                # 原始文本尺寸
                                original_text_width = max_width
                                original_text_height = total_height
                                font_debug_info.append(f"Original text dimensions: {original_text_width}x{original_text_height}px")
                                
                                # 添加文本宽度估算检查 - 防止文字变小
                                # 估算每个字符的平均宽度
                                avg_char_width = render_size * 0.7  # 大多数字体字符宽度约为字体大小的70%
                                
                                # 找到最长的一行
                                longest_line = max(lines, key=len) if lines else text_content
                                # 估算的最小宽度
                                estimated_min_width = len(longest_line) * avg_char_width * 0.8  # 给予20%的容错空间
                                
                                # 如果计算出的宽度异常小（小于估算宽度的80%），使用估算宽度
                                if original_text_width < estimated_min_width:
                                    font_debug_info.append(f"Width calculation issue detected: calculated={original_text_width}px, estimated={estimated_min_width}px")
                                    original_text_width = estimated_min_width
                                    font_debug_info.append(f"Using estimated width: {original_text_width}px")
                                
                                # 如果宽度仍然过小，设置一个最小值
                                min_absolute_width = render_size * 4  # 至少4个字符宽度
                                if original_text_width < min_absolute_width:
                                    font_debug_info.append(f"Width too small, using minimum width: {min_absolute_width}px")
                                    original_text_width = min_absolute_width
                                
                                # 放大系数，使文字更清晰
                                scale_factor = 2.0  # 增加到2倍以提高清晰度
                                
                                # 创建高分辨率图层用于渲染文字
                                hr_width = img_width * 2
                                hr_height = img_height * 2
                                hr_layer = Image.new('RGBA', (hr_width, hr_height), (0, 0, 0, 0))
                                hr_draw = ImageDraw.Draw(hr_layer)
                                
                                # 尝试创建高分辨率字体
                                hr_font = None
                                try:
                                    hr_font_size = render_size * 2
                                    if st.session_state.loaded_font_path:
                                        hr_font = ImageFont.truetype(st.session_state.loaded_font_path, hr_font_size)
                                        font_debug_info.append(f"Created high-res font: {hr_font_size}px")
                                except Exception as hr_font_err:
                                    font_debug_info.append(f"Failed to create high-res font: {str(hr_font_err)}")
                                
                                if hr_font is None:
                                    hr_font = font
                                    font_debug_info.append("Using original font for high-res rendering")
                                
                                # 高分辨率尺寸
                                hr_line_height = line_height * 2
                                hr_text_width = max_width * 2
                                hr_text_height = total_height * 2
                                
                                # 获取对齐方式并转换为小写
                                alignment = alignment.lower() if isinstance(alignment, str) else "center"
                                
                                # 根据对齐方式计算X位置
                                if alignment == "left":
                                    text_x = int(img_width * 0.2)
                                elif alignment == "right":
                                    text_x = int(img_width * 0.8 - original_text_width)
                                else:  # 居中
                                    text_x = (img_width - original_text_width) // 2
                                
                                # 垂直位置 - 上移以更好地展示在T恤上
                                text_y = int(img_height * 0.3 - original_text_height // 2)
                                
                                # 高分辨率位置
                                hr_text_x = text_x * 2
                                hr_text_y = text_y * 2
                                
                                font_debug_info.append(f"HR text position: ({hr_text_x}, {hr_text_y})")
                                
                                # 先应用特效 - 在高分辨率画布上
                                if "Outline" in text_style:
                                    # 增强轮廓效果
                                    outline_color = "black"
                                    outline_width = max(8, hr_font_size // 10)  # 加粗轮廓宽度
                                    
                                    # 多方向轮廓，让描边更均匀
                                    for angle in range(0, 360, 30):  # 每30度一个点，更平滑
                                        rad = math.radians(angle)
                                        offset_x = int(outline_width * math.cos(rad))
                                        offset_y = int(outline_width * math.sin(rad))
                                        
                                        # 处理多行文本
                                        for i, line in enumerate(lines):
                                            line_y = hr_text_y + i * hr_line_height
                                            if alignment == "center":
                                                line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                                line_width = line_bbox[2] - line_bbox[0]
                                                line_x = hr_text_x + (hr_text_width - line_width) // 2
                                            elif alignment == "right":
                                                line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                                line_width = line_bbox[2] - line_bbox[0]
                                                line_x = hr_text_x + (hr_text_width - line_width)
                                            else:
                                                line_x = hr_text_x
                                            
                                            hr_draw.text((line_x + offset_x, line_y + offset_y), 
                                                      line, fill=outline_color, font=hr_font)
                                
                                if "Shadow" in text_style:
                                    # 增强阴影效果
                                    shadow_color = (0, 0, 0, 150)  # 半透明黑色
                                    shadow_offset = max(15, hr_font_size // 8)  # 增加阴影偏移距离
                                    
                                    # 处理多行文本
                                    for i, line in enumerate(lines):
                                        line_y = hr_text_y + i * hr_line_height
                                        if alignment == "center":
                                            line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                            line_width = line_bbox[2] - line_bbox[0]
                                            line_x = hr_text_x + (hr_text_width - line_width) // 2
                                        elif alignment == "right":
                                            line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                            line_width = line_bbox[2] - line_bbox[0]
                                            line_x = hr_text_x + (hr_text_width - line_width)
                                        else:
                                            line_x = hr_text_x
                                        
                                        # 创建更平滑的阴影效果
                                        blur_steps = 8  # 更多步骤，更平滑的阴影
                                        for step in range(blur_steps):
                                            offset = shadow_offset * (step + 1) / blur_steps
                                            alpha = int(150 * (1 - step/blur_steps))
                                            cur_shadow = (0, 0, 0, alpha)
                                            hr_draw.text((line_x + offset, line_y + offset), 
                                                       line, fill=cur_shadow, font=hr_font)
                                
                                # 将文字颜色从十六进制转换为RGBA
                                text_rgb = tuple(int(text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                                text_rgba = text_rgb + (255,)  # 完全不透明
                                
                                # 绘制主文字 - 在高分辨率画布上
                                for i, line in enumerate(lines):
                                    line_y = hr_text_y + i * hr_line_height
                                    if alignment == "center":
                                        line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                        line_width = line_bbox[2] - line_bbox[0]
                                        line_x = hr_text_x + (hr_text_width - line_width) // 2
                                    elif alignment == "right":
                                        line_bbox = hr_draw.textbbox((0, 0), line, font=hr_font)
                                        line_width = line_bbox[2] - line_bbox[0]
                                        line_x = hr_text_x + (hr_text_width - line_width)
                                    else:
                                        line_x = hr_text_x
                                    
                                    hr_draw.text((line_x, line_y), line, fill=text_rgba, font=hr_font)
                                
                                # 特殊效果处理
                                if text_effect != "None":
                                    font_debug_info.append(f"Applying special effect: {text_effect}")
                                    # 未来可以在这里添加高分辨率特效处理
                                
                                # 将高分辨率图层缩小回原始尺寸 - 使用LANCZOS重采样以获得最佳质量
                                text_layer = hr_layer.resize((img_width, img_height), Image.LANCZOS)
                                font_debug_info.append("Downsampled high-res text layer to original size")
                                
                                # 应用文字到设计
                                new_design.paste(text_layer, (0, 0), text_layer)
                                
                                # 保存相关信息
                                st.session_state.text_position = (text_x, text_y)
                                st.session_state.text_size_info = {
                                    "font_size": render_size,
                                    "text_width": original_text_width,
                                    "text_height": original_text_height,
                                    "scale_factor": scale_factor
                                }
                                
                                # 保存文本图层的副本用于颜色变化时恢复
                                try:
                                    st.session_state.text_layer = text_layer.copy()
                                    font_debug_info.append("Text layer backup saved for color change restoration")
                                except Exception as e:
                                    font_debug_info.append(f"Failed to save text layer backup: {str(e)}")
                                
                                # 应用成功
                                font_debug_info.append("Text rendering applied successfully")
                                
                                # 更新设计和预览
                                st.session_state.final_design = new_design
                                st.session_state.current_image = new_design.copy()
                                
                                # 保存完整的文字信息
                                st.session_state.applied_text = {
                                    "text": text_content,
                                    "font": font_family,
                                    "color": text_color,
                                    "size": text_size,
                                    "style": text_style,
                                    "effect": text_effect,
                                    "alignment": alignment,
                                    "position": (text_x, text_y),
                                    "use_drawing_method": True
                                }
                                
                                # 保存字体加载和渲染信息
                                st.session_state.font_debug_info = font_debug_info
                                
                                # 显示成功消息
                                success_msg = f"""
                                Text applied to design successfully!
                                Font: {font_family}
                                Size: {render_size}px
                                Actual width: {original_text_width}px
                                Actual height: {original_text_height}px
                                Position: ({text_x}, {text_y})
                                T-shirt size: {img_width} x {img_height}
                                Rendering method: High-definition rendering
                                """
                                st.success(success_msg)
                                st.rerun()
                            else:
                                st.error("Failed to load any font. Cannot apply text.")
                        except Exception as e:
                            st.error(f"Error applying text: {str(e)}")
                            import traceback
                            st.error(traceback.format_exc())

        # Logo设计部分
        st.markdown("#### 🖼️ Logo Design")
        
        # 自动生成的Logo显示
        if hasattr(st.session_state, 'show_generated_logo') and st.session_state.show_generated_logo:
            st.markdown("**Current Logo:**")
            st.image(st.session_state.generated_logo, width=150)
            
            # 添加Logo调整选项
            logo_size = st.slider("Logo size:", 10, 50, 25, key="logo_size")
            logo_position = st.selectbox("Logo position:", 
                ["Top-left", "Top-center", "Top-right", "Center", "Bottom-left", "Bottom-center", "Bottom-right"],
                index=3, key="logo_position")
            logo_opacity = st.slider("Logo opacity:", 0, 100, 100, key="logo_opacity")
            
            # 添加手动应用Logo的按钮
            if st.button("Apply Logo to Design"):
                try:
                    # 获取当前图像
                    if st.session_state.final_design is not None:
                        new_design = st.session_state.final_design.copy()
                    else:
                        new_design = st.session_state.base_image.copy()
                    
                    # 获取图像尺寸
                    img_width, img_height = new_design.size
                    
                    # 定义T恤前胸区域
                    chest_width = int(img_width * 0.95)
                    chest_height = int(img_height * 0.6)
                    chest_left = (img_width - chest_width) // 2
                    chest_top = int(img_height * 0.2)
                    
                    # 调整Logo大小
                    logo_size_factor = logo_size / 100
                    logo_width = int(chest_width * logo_size_factor * 0.5)
                    logo_height = int(logo_width * st.session_state.generated_logo.height / st.session_state.generated_logo.width)
                    logo_resized = st.session_state.generated_logo.resize((logo_width, logo_height), Image.LANCZOS)
                    
                    # 位置映射
                    position_mapping = {
                        "Top-left": (chest_left + 10, chest_top + 10),
                        "Top-center": (chest_left + (chest_width - logo_width) // 2, chest_top + 10),
                        "Top-right": (chest_left + chest_width - logo_width - 10, chest_top + 10),
                        "Center": (chest_left + (chest_width - logo_width) // 2, chest_top + (chest_height - logo_height) // 2),
                        "Bottom-left": (chest_left + 10, chest_top + chest_height - logo_height - 10),
                        "Bottom-center": (chest_left + (chest_width - logo_width) // 2, chest_top + chest_height - logo_height - 10),
                        "Bottom-right": (chest_left + chest_width - logo_width - 10, chest_top + chest_height - logo_height - 10)
                    }
                    
                    logo_x, logo_y = position_mapping.get(logo_position, (chest_left + 10, chest_top + 10))
                    
                    # 设置透明度
                    if logo_opacity < 100:
                        logo_data = logo_resized.getdata()
                        new_data = []
                        for item in logo_data:
                            r, g, b, a = item
                            new_a = int(a * logo_opacity / 100)
                            new_data.append((r, g, b, new_a))
                        logo_resized.putdata(new_data)
                    
                    # 粘贴Logo到设计
                    try:
                        # 确保图像处于RGBA模式以支持透明度
                        final_design_rgba = new_design.convert("RGBA")
                        
                        # 创建临时图像，用于粘贴logo
                        temp_image = Image.new("RGBA", final_design_rgba.size, (0, 0, 0, 0))
                        temp_image.paste(logo_resized, (logo_x, logo_y), logo_resized)
                        
                        # 使用alpha_composite合成图像
                        final_design = Image.alpha_composite(final_design_rgba, temp_image)
                        
                        # 更新最终设计和当前图像
                        st.session_state.final_design = final_design
                        st.session_state.current_image = final_design.copy()
                        
                        # 保存Logo信息
                        st.session_state.applied_logo = {
                            "source": "ai",
                            "path": "temp_logo.png",
                            "size": logo_size,
                            "position": logo_position,
                            "opacity": logo_opacity
                        }
                        
                        st.success("Logo has been applied to the design successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Logo合成时出错: {str(e)}")
                except Exception as e:
                    st.error(f"应用Logo时出错: {str(e)}")
            
            # 添加分隔线
            st.markdown("---")
        
        # 添加Logo提示词输入框（默认为空）
        logo_prompt = st.text_input(
            "Enter logo description",
            value="",
            key="logo_prompt_input"
        )
        
        # 添加生成Logo的按钮
        if st.button("Generate Logo"):
            if logo_prompt:
                with st.spinner("Generating logo..."):
                    try:
                        # 构建完整的提示词
                        full_prompt = f"Create a Logo design: {logo_prompt}. Requirements: 1. Use a clean and professional design 2. Suitable for printing on T-shirts 3. Clear and recognizable图案清晰可识别 4. No transparent background 5. Ensure good contrast and visibility"
                        
                        # 调用DALL-E生成图像
                        new_logo = generate_vector_image(full_prompt)
                        
                        if new_logo:
                            # 保存新生成的Logo
                            st.session_state.generated_logo = new_logo
                            st.session_state.logo_prompt = logo_prompt
                            st.session_state.logo_auto_generated = True
                            st.session_state.show_generated_logo = True
                            
                            # 如果当前设计中已经有Logo，需要移除旧的Logo并应用新的Logo
                            if hasattr(st.session_state, 'applied_logo') and st.session_state.applied_logo is not None:
                                try:
                                    # 获取当前图像
                                    if st.session_state.final_design is not None:
                                        new_design = st.session_state.final_design.copy()
                                    else:
                                        new_design = st.session_state.base_image.copy()
                                    
                                    # 获取图像尺寸
                                    img_width, img_height = new_design.size
                                    
                                    # 定义T恤前胸区域
                                    chest_width = int(img_width * 0.95)
                                    chest_height = int(img_height * 0.6)
                                    chest_left = (img_width - chest_width) // 2
                                    chest_top = int(img_height * 0.2)
                                    
                                    # 使用当前Logo的大小和位置设置
                                    logo_size = st.session_state.applied_logo.get("size", 25)
                                    logo_position = st.session_state.applied_logo.get("position", "Center")
                                    logo_opacity = st.session_state.applied_logo.get("opacity", 100)
                                    
                                    # 调整新Logo大小
                                    logo_size_factor = logo_size / 100
                                    logo_width = int(chest_width * logo_size_factor * 0.5)
                                    logo_height = int(logo_width * new_logo.height / new_logo.width)
                                    logo_resized = new_logo.resize((logo_width, logo_height), Image.LANCZOS)
                                    
                                    # 位置映射
                                    position_mapping = {
                                        "Top-left": (chest_left + 10, chest_top + 10),
                                        "Top-center": (chest_left + (chest_width - logo_width) // 2, chest_top + 10),
                                        "Top-right": (chest_left + chest_width - logo_width - 10, chest_top + 10),
                                        "Center": (chest_left + (chest_width - logo_width) // 2, chest_top + (chest_height - logo_height) // 2),
                                        "Bottom-left": (chest_left + 10, chest_top + chest_height - logo_height - 10),
                                        "Bottom-center": (chest_left + (chest_width - logo_width) // 2, chest_top + chest_height - logo_height - 10),
                                        "Bottom-right": (chest_left + chest_width - logo_width - 10, chest_top + chest_height - logo_height - 10)
                                    }
                                    
                                    logo_x, logo_y = position_mapping.get(logo_position, (chest_left + 10, chest_top + 10))
                                    
                                    # 设置透明度
                                    if logo_opacity < 100:
                                        logo_data = logo_resized.getdata()
                                        new_data = []
                                        for item in logo_data:
                                            r, g, b, a = item
                                            new_a = int(a * logo_opacity / 100)
                                            new_data.append((r, g, b, new_a))
                                        logo_resized.putdata(new_data)
                                    
                                    # 粘贴新Logo到设计
                                    try:
                                        # 确保图像处于RGBA模式以支持透明度
                                        final_design_rgba = new_design.convert("RGBA")
                                        
                                        # 创建临时图像，用于粘贴logo
                                        temp_image = Image.new("RGBA", final_design_rgba.size, (0, 0, 0, 0))
                                        temp_image.paste(logo_resized, (logo_x, logo_y), logo_resized)
                                        
                                        # 使用alpha_composite合成图像
                                        final_design = Image.alpha_composite(final_design_rgba, temp_image)
                                        
                                        # 更新最终设计和当前图像
                                        st.session_state.final_design = final_design
                                        st.session_state.current_image = final_design.copy()
                                        
                                        # 更新Logo信息
                                        st.session_state.applied_logo = {
                                            "source": "ai",
                                            "path": "temp_logo.png",
                                            "size": logo_size,
                                            "position": logo_position,
                                            "opacity": logo_opacity,
                                            "prompt": logo_prompt
                                        }
                                        
                                        st.success("New logo has been generated and applied to your design!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error applying new logo: {str(e)}")
                                except Exception as e:
                                    st.error(f"Error updating design with new logo: {str(e)}")
                            else:
                                st.success("New logo has been generated successfully!")
                                st.rerun()
                        else:
                            st.error("Failed to generate new logo, please try again.")
                    except Exception as e:
                        st.error(f"Error generating new logo: {str(e)}")
            else:
                st.warning("Please enter a logo description.")
