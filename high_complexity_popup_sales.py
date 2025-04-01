import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os  # 确保os模块在这里导入
# 添加try-except导入cairosvg，避免因缺少这个库而导致整个应用崩溃
try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False
    # 尝试导入备选SVG处理库
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        SVGLIB_AVAILABLE = True
    except ImportError:
        SVGLIB_AVAILABLE = False
        st.warning("SVG处理库未安装，SVG格式转换功能将不可用")
from openai import OpenAI
from streamlit_image_coordinates import streamlit_image_coordinates
import re
import math
# 导入面料纹理模块
from fabric_texture import apply_fabric_texture

# API配置信息 - 实际使用时应从主文件传入或使用环境变量
API_KEY = "sk-lNVAREVHjj386FDCd9McOL7k66DZCUkTp6IbV0u9970qqdlg"
BASE_URL = "https://api.deepbricks.ai/v1/"

# GPT-4o-mini API配置
GPT4O_MINI_API_KEY = "sk-lNVAREVHjj386FDCd9McOL7k66DZCUkTp6IbV0u9970qqdlg"
GPT4O_MINI_BASE_URL = "https://api.deepbricks.ai/v1/"

# 从svg_utils导入SVG转换函数
from svg_utils import convert_svg_to_png

def get_ai_design_suggestions(user_preferences=None):
    """Get design suggestions from GPT-4o-mini"""
    client = OpenAI(api_key=GPT4O_MINI_API_KEY, base_url=GPT4O_MINI_BASE_URL)
    
    # Default prompt if no user preferences provided
    if not user_preferences:
        user_preferences = "casual fashion t-shirt design"
    
    # Construct the prompt
    prompt = f"""
    As a T-shirt design consultant, please provide the following design suggestions for the "{user_preferences}" style:

    1. Color Suggestions: Recommend 3 suitable colors, including:
       - Color name and hex code (e.g., Blue (#0000FF))
       - Why this color suits the style (2-3 sentences explanation)
       
    2. Fabric Texture Suggestions: Recommend 2 suitable fabric types, including:
       - Specific fabric name (Cotton, Polyester, Cotton-Polyester Blend, Jersey, Linen, or Bamboo)
       - Brief explanation on why this fabric suits the style
       
    3. Text Suggestions: Recommend 2 suitable texts/phrases:
       - Specific text content
       - Recommended font style
       - Brief explanation of suitability
       
    4. Logo Element Suggestions: Recommend 2 suitable design elements:
       - Element description
       - How it complements the overall style
       
    Please ensure to include hex codes for colors, keep content detailed but concise.
    For text suggestions, place each recommended phrase/text on a separate line and wrap them in quotes, e.g., "Just Do It".
    """
    
    try:
        # 调用GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional T-shirt design consultant, providing useful and specific suggestions. Include sufficient details to help users understand your recommendations, while avoiding unnecessary verbosity. Ensure to include hex codes for each color. For text suggestions, please wrap recommended phrases in quotes and place them on separate lines."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # 返回建议内容
        if response.choices and len(response.choices) > 0:
            suggestion_text = response.choices[0].message.content
            
            # 尝试解析颜色代码
            try:
                # 提取颜色代码的简单方法
                color_matches = {}
                
                # 查找形如 "颜色名 (#XXXXXX)" 的模式
                color_pattern = r'([^\s\(\)]+)\s*\(#([0-9A-Fa-f]{6})\)'
                matches = re.findall(color_pattern, suggestion_text)
                
                if matches:
                    color_matches = {name.strip(): f"#{code}" for name, code in matches}
                    
                # 保存到会话状态
                if color_matches:
                    st.session_state.ai_suggested_colors = color_matches
                    
                # 尝试提取推荐文字
                text_pattern = r'[""]([^""]+)[""]'
                text_matches = re.findall(text_pattern, suggestion_text)
                
                # 保存推荐文字到会话状态
                if text_matches:
                    st.session_state.ai_suggested_texts = text_matches
                else:
                    # 尝试使用另一种模式匹配
                    text_pattern2 = r'"([^"]+)"'
                    text_matches = re.findall(text_pattern2, suggestion_text)
                    if text_matches:
                        st.session_state.ai_suggested_texts = text_matches
                    else:
                        st.session_state.ai_suggested_texts = []
                
                # 提取推荐面料类型
                fabric_types = ["Cotton", "Polyester", "Cotton-Polyester Blend", "Jersey", "Linen", "Bamboo"]
                fabric_matches = {}
                
                for fabric in fabric_types:
                    if fabric in suggestion_text:
                        # 尝试提取该面料周围的一段文本作为描述
                        start_idx = suggestion_text.find(fabric)
                        end_idx = min(start_idx + 200, len(suggestion_text))
                        desc_text = suggestion_text[start_idx:end_idx]
                        # 尝试在这段文本中找一个句子作为描述
                        sentence_end = re.search(r'\.(?=\s|$)', desc_text)
                        if sentence_end:
                            desc = desc_text[:sentence_end.end()].strip()
                        else:
                            desc = desc_text.split('\n')[0].strip()
                        fabric_matches[fabric] = desc
                
                # 保存推荐面料到会话状态
                if fabric_matches:
                    st.session_state.ai_suggested_fabrics = fabric_matches
                
                # 提取Logo建议
                logo_pattern = r'(?:Logo Element Suggestions|Logo|design elements?):(.*?)(?:\d\.|$)'
                logo_section_match = re.search(logo_pattern, suggestion_text, re.DOTALL | re.IGNORECASE)
                
                if logo_section_match:
                    logo_section = logo_section_match.group(1).strip()
                    # 提取单个Logo描述
                    logo_desc_pattern = r'(?:-|\d+\.)\s*(.*?)(?=(?:-|\d+\.)|$)'
                    logo_descriptions = re.findall(logo_desc_pattern, logo_section, re.DOTALL)
                    
                    if logo_descriptions:
                        # 清理描述（去除多余空格和换行）
                        cleaned_descriptions = [re.sub(r'\s+', ' ', desc.strip()) for desc in logo_descriptions]
                        # 保存到会话状态
                        st.session_state.ai_suggested_logos = cleaned_descriptions
                        
                        # 自动生成第一个Logo
                        try:
                            if cleaned_descriptions and len(cleaned_descriptions) > 0:
                                # 获取第一个Logo描述
                                first_logo_desc = cleaned_descriptions[0]
                                # 构建完整的提示词
                                full_prompt = f"Create a Logo design: {first_logo_desc}. Requirements: 1. Use a simple design 2. Suitable for printing 3. Background transparent 4. Clear and recognizable图案清晰可识别"
                                
                                # 调用DALL-E生成图像
                                logo_image = generate_vector_image(full_prompt)
                                
                                if logo_image:
                                    # 保存生成的Logo
                                    st.session_state.generated_logo = logo_image
                                    # 保存Logo提示词
                                    st.session_state.logo_prompt = first_logo_desc
                                    # 记录logo是自动生成的
                                    st.session_state.logo_auto_generated = True
                                    # 添加一个变量记录需要在UI中显示Logo
                                    st.session_state.show_generated_logo = True
                                    
                                    # 在控制台打印日志以便调试
                                    print(f"Logo自动生成成功: {first_logo_desc}")
                        except Exception as logo_gen_error:
                            print(f"自动生成Logo时出错: {logo_gen_error}")
                            # 如果自动生成失败，不阻止其他功能
                    
            except Exception as e:
                print(f"Error parsing: {e}")
                st.session_state.ai_suggested_texts = []
                
            # 使用更好的排版处理文本
            # 替换标题格式
            formatted_text = suggestion_text
            # 处理序号段落
            formatted_text = re.sub(r'(\d\. .*?)(?=\n\d\. |\n*$)', r'<div class="suggestion-section">\1</div>', formatted_text)
            # 处理子项目符号
            formatted_text = re.sub(r'- (.*?)(?=\n- |\n[^-]|\n*$)', r'<div class="suggestion-item">• \1</div>', formatted_text)
            # 强调颜色名称和代码
            formatted_text = re.sub(r'([^\s\(\)]+)\s*\(#([0-9A-Fa-f]{6})\)', r'<span class="color-name">\1</span> <span class="color-code">(#\2)</span>', formatted_text)
            
            # 不再使用JavaScript回调，而是简单地加粗文本
            formatted_text = re.sub(r'[""]([^""]+)[""]', r'"<strong>\1</strong>"', formatted_text)
            formatted_text = re.sub(r'"([^"]+)"', r'"<strong>\1</strong>"', formatted_text)
            
            suggestion_with_style = f"""
            <div class="suggestion-container">
            {formatted_text}
            </div>
            """
            
            # 打印调试信息，确认Logo是否自动生成
            if hasattr(st.session_state, 'generated_logo'):
                print("Logo generated successfully and saved to session_state")
            else:
                print("Failed to generate Logo or not saved to session_state")
            
            return suggestion_with_style
        else:
            return "can not get AI suggestions, please try again later."
    except Exception as e:
        return f"Error getting AI suggestions: {str(e)}"

def generate_vector_image(prompt):
    """Generate an image based on the prompt"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    try:
        resp = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
    except Exception as e:
        st.error(f"Error calling API: {e}")
        return None

    if resp and len(resp.data) > 0 and resp.data[0].url:
        image_url = resp.data[0].url
        try:
            image_resp = requests.get(image_url)
            if image_resp.status_code == 200:
                content_type = image_resp.headers.get("Content-Type", "")
                if "svg" in content_type.lower():
                    # 使用集中的SVG处理函数
                    return convert_svg_to_png(image_resp.content)
                else:
                    return Image.open(BytesIO(image_resp.content)).convert("RGBA")
            else:
                st.error(f"Failed to download image, status code: {image_resp.status_code}")
        except Exception as download_err:
            st.error(f"Error requesting image: {download_err}")
    else:
        st.error("Could not get image URL from API response.")
    return None

def draw_selection_box(image, point=None):
    """Calculate position for design placement without drawing visible selection box"""
    # Create a copy to avoid modifying the original image
    img_copy = image.copy()
    
    # Fixed box size (1024 * 0.25)
    box_size = int(1024 * 0.25)
    
    # If no position is specified, place it in the center
    if point is None:
        x1 = (image.width - box_size) // 2
        y1 = (image.height - box_size) // 2
    else:
        x1, y1 = point
        # Ensure the selection box doesn't extend beyond image boundaries
        x1 = max(0, min(x1 - box_size//2, image.width - box_size))
        y1 = max(0, min(y1 - box_size//2, image.height - box_size))
    
    # Return the image without drawing any visible box, just the position
    return img_copy, (x1, y1)

def get_selection_coordinates(point=None, image_size=None):
    """Get coordinates and dimensions of fixed-size selection box"""
    box_size = int(1024 * 0.25)
    
    if point is None and image_size is not None:
        width, height = image_size
        x1 = (width - box_size) // 2
        y1 = (height - box_size) // 2
    else:
        x1, y1 = point
        # Ensure selection box doesn't extend beyond image boundaries
        if image_size:
            width, height = image_size
            x1 = max(0, min(x1 - box_size//2, width - box_size))
            y1 = max(0, min(y1 - box_size//2, height - box_size))
    
    return (x1, y1, box_size, box_size)

def match_background_to_shirt(design_image, shirt_image):
    """Adjust design image background color to match shirt"""
    # Ensure images are in RGBA mode
    design_image = design_image.convert("RGBA")
    shirt_image = shirt_image.convert("RGBA")
    
    # Get shirt background color (assuming top-left corner color)
    shirt_bg_color = shirt_image.getpixel((0, 0))
    
    # Get design image data
    datas = design_image.getdata()
    newData = []
    
    for item in datas:
        # If pixel is transparent, keep it unchanged
        if item[3] == 0:
            newData.append(item)
        else:
            # Adjust non-transparent pixel background color to match shirt
            newData.append((shirt_bg_color[0], shirt_bg_color[1], shirt_bg_color[2], item[3]))
    
    design_image.putdata(newData)
    return design_image

# 添加一个用于改变T恤颜色的函数
def change_shirt_color(image, color_hex, apply_texture=False, fabric_type=None):
    """改变T恤的颜色，可选择应用面料纹理"""
    # 判断是否是应用了纹理的图像，如果是，则重新从原始图像开始处理
    # 这可以确保每次更改颜色时都从原始状态开始，而不是在已应用纹理的图像上再次修改
    if hasattr(st.session_state, 'original_base_image') and st.session_state.original_base_image is not None:
        # 使用原始白色T恤图像作为基础
        image = st.session_state.original_base_image.copy()
    
    # 转换十六进制颜色为RGB
    color_rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # 创建副本避免修改原图
    colored_image = image.copy().convert("RGBA")
    
    # 获取图像数据
    data = colored_image.getdata()
    
    # 创建新数据
    new_data = []
    # 白色阈值 - 调整这个值可以控制哪些像素被视为白色/浅色并被改变
    threshold = 200
    
    for item in data:
        # 判断是否是白色/浅色区域 (RGB值都很高)
        if item[0] > threshold and item[1] > threshold and item[2] > threshold and item[3] > 0:
            # 保持原透明度，改变颜色
            new_color = (color_rgb[0], color_rgb[1], color_rgb[2], item[3])
            new_data.append(new_color)
        else:
            # 保持其他颜色不变
            new_data.append(item)
    
    # 更新图像数据
    colored_image.putdata(new_data)
    
    # 如果需要应用纹理
    if apply_texture and fabric_type:
        return apply_fabric_texture(colored_image, fabric_type)
    
    return colored_image

def get_preset_logos():
    """获取预设logo文件夹中的所有图片"""
    # 确保os模块在这个作用域内可用
    import os
    
    logos_dir = "logos"
    preset_logos = []
    
    # 检查logos文件夹是否存在
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
        return preset_logos
    
    # 获取所有支持的图片文件
    for file in os.listdir(logos_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            preset_logos.append(os.path.join(logos_dir, file))
    
    return preset_logos

# AI Customization Group design page
def show_high_complexity_popup_sales():
    st.title("👕 AI Co-Creation Experiment Platform")
    st.markdown("### High Task Complexity-Popup Sales - Create Your Unique T-shirt Design")
    
    # 添加General Sales情境描述
    st.info("""
    **Popup Sales Environment**
    
    Welcome to our regular T-shirt customization service available in our standard online store. 
    You are browsing our website from the comfort of your home or office, with no time pressure. 
    Take your time to explore the design options and create a T-shirt that matches your personal style.
    This is a typical online shopping experience where you can customize at your own pace.
    """)
    
    # 任务复杂度说明
    st.markdown("""
    <div style="background-color:#f0f0f0; padding:20px; border-radius:10px; margin-bottom:20px; border-left:4px solid #2196F3">
    <h4 style="color:#1976D2; margin-top:0">Basic Customization Options</h4>
    <p>In this experience, you can customize your T-shirt with the following options:</p>
    
    <div style="margin-left:15px">
    <h5 style="color:#2196F3">1. T-shirt Color Selection</h5>
    <p>Choose your preferred T-shirt color from AI recommendations, preset options, or use a custom color picker to find the perfect shade for your design.</p>
    
    <h5 style="color:#2196F3">2. Text Customization</h5>
    <p>Add personalized text with customizable font styles, sizes, colors, and special effects like shadows, outlines, or gradients to create eye-catching designs.</p>
    
    <h5 style="color:#2196F3">3. Logo Integration</h5>
    <p>Enhance your design by uploading your own logo or selecting from our preset collection, with options to adjust size, position, and transparency.</p>
    
    <h5 style="color:#2196F3">4. Design Positioning</h5>
    <p>Fine-tune the placement of your text and logo elements using intuitive positioning controls and preset alignment options for perfect composition.</p>
    </div>
    
    <p style="margin-top:15px; color:#666">
    <i>💡 Tip: Start with AI suggestions for the best results, then customize further based on your preferences.</i>
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化T恤颜色和纹理状态变量
    if 'shirt_color_hex' not in st.session_state:
        st.session_state.shirt_color_hex = "#FFFFFF"  # 默认白色
    if 'current_applied_color' not in st.session_state:
        st.session_state.current_applied_color = st.session_state.shirt_color_hex  # 初始应用的颜色
    if 'current_applied_fabric' not in st.session_state:
        st.session_state.current_applied_fabric = st.session_state.fabric_type  # 初始应用的纹理
    if 'original_base_image' not in st.session_state:
        st.session_state.original_base_image = None  # 保存原始白色T恤图像
    if 'base_image' not in st.session_state:
        st.session_state.base_image = None  # 确保base_image变量被初始化
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None  # 确保current_image变量被初始化
    if 'final_design' not in st.session_state:
        st.session_state.final_design = None  # 确保final_design变量被初始化
    if 'ai_suggestions' not in st.session_state:
        st.session_state.ai_suggestions = None  # 存储AI建议
    
    # 重新组织布局，将预览图放在左侧，操作区放在右侧
    st.markdown("## Design Area")
    
    # 创建左右两列布局
    preview_col, controls_col = st.columns([3, 2])
    
    with preview_col:
        # T恤预览区
        st.markdown("### T-shirt Design")
        
        # Load T-shirt base image
        if st.session_state.base_image is None:
            try:
                # 确保os模块在这个作用域内可用
                import os
                
                # 加载原始白色T恤图像
                original_image_path = "white_shirt.png"
                # 检查各种可能的路径
                possible_paths = [
                    "white_shirt.png",
                    "./white_shirt.png",
                    "../white_shirt.png",
                    "low_complexity_general_sales_files/white_shirt.png",
                    "images/white_shirt.png",
                    "white_shirt1.png",
                    "white_shirt2.png"
                ]
                
                # 尝试所有可能的路径
                found = False
                for path in possible_paths:
                    if os.path.exists(path):
                        original_image_path = path
                        found = True
                        break
                
                if not found:
                    # 如果未找到，显示当前工作目录和文件列表以便调试
                    current_dir = os.getcwd()
                    st.error(f"T-shirt image not found. Current working directory: {current_dir}")
                    files = os.listdir(current_dir)
                    st.error(f"Directory contents: {files}")
                
                # 加载原始白色T恤图像
                original_image = Image.open(original_image_path).convert("RGBA")
                
                # 保存原始白色T恤图像
                st.session_state.original_base_image = original_image.copy()
                
                # 应用当前选择的颜色和纹理
                colored_image = change_shirt_color(
                    original_image, 
                    st.session_state.shirt_color_hex,
                    apply_texture=True,  # 默认应用纹理
                    fabric_type=st.session_state.fabric_type  # 使用当前选择的面料
                )
                st.session_state.base_image = colored_image
                
                # Initialize by drawing selection box in the center
                initial_image, initial_pos = draw_selection_box(colored_image)
                st.session_state.current_image = initial_image
                st.session_state.current_box_position = initial_pos
                
                # 设置初始最终设计为彩色T恤
                st.session_state.final_design = colored_image.copy()
            except Exception as e:
                st.error(f"Error loading t-shirt image: {e}")
                import traceback
                st.error(traceback.format_exc())
        else:
            # 添加颜色变化检测：保存当前应用的颜色，用于检查是否发生变化
            if 'current_applied_color' not in st.session_state:
                st.session_state.current_applied_color = st.session_state.shirt_color_hex
            
            # 添加纹理变化检测：保存当前应用的纹理，用于检查是否发生变化
            if 'current_applied_fabric' not in st.session_state:
                st.session_state.current_applied_fabric = st.session_state.fabric_type
            
            # 检测设计变化（颜色或纹理变化）
            if (st.session_state.current_applied_color != st.session_state.shirt_color_hex or 
                st.session_state.current_applied_fabric != st.session_state.fabric_type):
                
                # 打印调试信息
                print(f"检测到设计变化:")
                print(f"- 颜色: {st.session_state.current_applied_color} -> {st.session_state.shirt_color_hex}")
                print(f"- 纹理: {st.session_state.current_applied_fabric} -> {st.session_state.fabric_type}")
                
                # 颜色或纹理已变化，需要重新应用
                original_image = st.session_state.original_base_image.copy()
            
            # 检查颜色是否发生变化
            if st.session_state.current_applied_color != st.session_state.shirt_color_hex:
                print(f"检测到颜色变化: {st.session_state.current_applied_color} -> {st.session_state.shirt_color_hex}")
                # 颜色已变化，需要重新应用
                original_image = st.session_state.original_base_image.copy()
                
                # 保存当前设计元素
                has_logo = hasattr(st.session_state, 'applied_logo') and st.session_state.applied_logo is not None
                temp_logo = None
                temp_logo_info = None
                
                # 更详细地检查Logo状态并保存
                if has_logo:
                    print("检测到已应用Logo，准备保存")
                    temp_logo_info = st.session_state.applied_logo.copy()
                    # 无论是自动生成还是用户生成，都应该保存到generated_logo中
                    if hasattr(st.session_state, 'generated_logo') and st.session_state.generated_logo is not None:
                        try:
                            temp_logo = st.session_state.generated_logo.copy()
                            print(f"成功复制Logo图像，尺寸: {temp_logo.size}")
                        except Exception as e:
                            print(f"复制Logo图像时出错: {e}")
                            temp_logo = None
                    else:
                        print("找不到generated_logo，无法保存Logo图像")
                else:
                    print("未检测到已应用的Logo")
                
                # 应用新颜色和纹理
                colored_image = change_shirt_color(
                    original_image, 
                    st.session_state.shirt_color_hex,
                    apply_texture=True,  # 应用纹理
                    fabric_type=st.session_state.fabric_type  # 使用当前选择的面料
                )
                st.session_state.base_image = colored_image
                
                # 更新当前图像和位置
                new_image, _ = draw_selection_box(colored_image, st.session_state.current_box_position)
                st.session_state.current_image = new_image
                
                # 设置为当前设计
                st.session_state.final_design = colored_image.copy()
                
                # 更新已应用的颜色和纹理
                st.session_state.current_applied_color = st.session_state.shirt_color_hex
                st.session_state.current_applied_fabric = st.session_state.fabric_type
                
                # 如果有Logo，重新应用Logo - 确保逻辑更严谨
                if has_logo and temp_logo is not None and temp_logo_info is not None:
                    try:
                        print("开始重新应用Logo...")
                        # 获取Logo信息
                        logo_prompt = temp_logo_info.get("prompt", "")
                        logo_size = temp_logo_info.get("size", 40)
                        logo_position = temp_logo_info.get("position", "Center")
                        logo_opacity = temp_logo_info.get("opacity", 100)
                        
                        print(f"Logo参数 - 提示词: {logo_prompt}, 大小: {logo_size}%, 位置: {logo_position}, 透明度: {logo_opacity}%")
                        
                        # 获取图像尺寸
                        img_width, img_height = st.session_state.final_design.size
                        
                        # 定义T恤前胸区域
                        chest_width = int(img_width * 0.95)
                        chest_height = int(img_height * 0.6)
                        chest_left = (img_width - chest_width) // 2
                        chest_top = int(img_height * 0.2)
                        
                        # 调整Logo大小
                        logo_size_factor = logo_size / 100
                        logo_width = int(chest_width * logo_size_factor * 0.5)
                        logo_height = int(logo_width * temp_logo.height / temp_logo.width)
                        logo_resized = temp_logo.resize((logo_width, logo_height), Image.LANCZOS)
                        
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
                        print(f"Logo位置: ({logo_x}, {logo_y}), 尺寸: {logo_width}x{logo_height}")
                        
                        # 设置透明度
                        if logo_opacity < 100:
                            logo_data = logo_resized.getdata()
                            new_data = []
                            for item in logo_data:
                                r, g, b, a = item
                                new_a = int(a * logo_opacity / 100)
                                new_data.append((r, g, b, new_a))
                            logo_resized.putdata(new_data)
                            print(f"已调整Logo透明度为: {logo_opacity}%")
                        
                        # 粘贴Logo到新设计
                        try:
                            # 确保图像处于RGBA模式以支持透明度
                            final_design_rgba = st.session_state.final_design.convert("RGBA")
                            
                            # 创建临时图像，用于粘贴logo
                            temp_image = Image.new("RGBA", final_design_rgba.size, (0, 0, 0, 0))
                            temp_image.paste(logo_resized, (logo_x, logo_y), logo_resized)
                            
                            # 使用alpha_composite合成图像
                            final_design = Image.alpha_composite(final_design_rgba, temp_image)
                            st.session_state.final_design = final_design
                        except Exception as e:
                            st.warning(f"Logo pasting failed: {e}")
                        
                        # 更新当前图像
                        st.session_state.current_image = st.session_state.final_design.copy()
                        
                        # 重新保存Logo信息和图像
                        st.session_state.applied_logo = temp_logo_info
                        st.session_state.generated_logo = temp_logo  # 确保保存回原始Logo
                        
                        print(f"Logo重新应用成功: {logo_prompt}")
                    except Exception as e:
                        print(f"重新应用Logo时出错: {e}")
                        import traceback
                        print(traceback.format_exc())
                    else:
                        if has_logo:
                            if temp_logo is None:
                                print("错误: 保存的Logo图像为空")
                            if temp_logo_info is None:
                                print("错误: 保存的Logo信息为空")
                        else:
                            print("无需重新应用Logo(未应用过)")
                
                # 修改颜色变更时重新应用文字的代码
                if 'applied_text' in st.session_state:
                    text_info = st.session_state.applied_text
                    
                    # 确保text_info存在且包含必要的信息
                    if text_info and isinstance(text_info, dict):
                        # 如果使用了绘图方法，同样以绘图方法重新应用
                        if text_info.get("use_drawing_method", False):
                            try:
                                # 图像尺寸
                                img_width, img_height = st.session_state.final_design.size
                                
                                # 创建小图像用于绘制文字
                                initial_text_width = min(400, img_width // 2)
                                initial_text_height = 200
                                text_img = Image.new('RGBA', (initial_text_width, initial_text_height), (0, 0, 0, 0))
                                text_draw = ImageDraw.Draw(text_img)
                                
                                # 加载字体
                                from PIL import ImageFont
                                import os
                                
                                # 创建text_info对象来存储文本信息
                                text_info = {
                                    "text": text_info["text"],
                                    "font": text_info["font"],
                                    "color": text_info["color"],
                                    "size": text_info["size"],
                                    "style": text_info["style"],
                                    "effect": text_info["effect"],
                                    "alignment": text_info["alignment"]
                                }
                                
                                # 尝试加载系统字体
                                font = None
                                try:
                                    # 确保os模块可用
                                    import os
                                    # 尝试直接加载系统字体
                                    if os.path.exists("C:/Windows/Fonts/arial.ttf"):
                                        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
                                except Exception:
                                    pass
                                
                                # 如果系统字体加载失败，使用默认字体
                                if font is None:
                                    font = ImageFont.load_default()
                                
                                # 在小图像上绘制文字
                                small_text_x = initial_text_width // 2
                                small_text_y = initial_text_height // 2
                                
                                # 应用效果
                                if "style" in text_info:
                                    if "轮廓" in text_info["style"]:
                                        offset = 2
                                        for offset_x, offset_y in [(offset,0), (-offset,0), (0,offset), (0,-offset)]:
                                            text_draw.text((small_text_x + offset_x, small_text_y + offset_y), 
                                                          text_info["text"], fill="black", font=font, anchor="mm")
                                    
                                    if "阴影" in text_info["style"]:
                                        shadow_offset = 4
                                        text_draw.text((small_text_x + shadow_offset, small_text_y + shadow_offset), 
                                                      text_info["text"], fill=(0, 0, 0, 180), font=font, anchor="mm")
                                
                                # 绘制主文字
                                text_draw.text((small_text_x, small_text_y), text_info["text"], 
                                              fill=text_info["color"], font=font, anchor="mm")
                                
                                # 裁剪图像
                                bbox = text_img.getbbox()
                                if bbox:
                                    text_img = text_img.crop(bbox)
                                
                                # 计算放大比例
                                scale_factor = text_info["size"] / 40
                                new_width = max(int(text_img.width * scale_factor), 10)
                                new_height = max(int(text_img.height * scale_factor), 10)
                                
                                # 放大文字图像
                                text_img_resized = text_img.resize((new_width, new_height), Image.LANCZOS)
                                
                                # 计算位置
                                if text_info["alignment"] == "left":
                                    paste_x = int(img_width * 0.2)
                                elif text_info["alignment"] == "right":
                                    paste_x = int(img_width * 0.8 - text_img_resized.width)
                                else:  # 居中
                                    paste_x = (img_width - text_img_resized.width) // 2
                                
                                # 垂直位置
                                paste_y = int(img_height * 0.4 - text_img_resized.height // 2)
                                
                                # 粘贴到T恤上
                                st.session_state.final_design.paste(text_img_resized, (paste_x, paste_y), text_img_resized)
                                st.session_state.current_image = st.session_state.final_design.copy()
                                
                                # 更新位置信息
                                st.session_state.applied_text["position"] = (paste_x, paste_y)
                                
                            except Exception as e:
                                st.warning(f"Error reapplying text using drawing method: {e}")
                                import traceback
                                st.warning(traceback.format_exc())
                        else:
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
                                    
                                    # 创建小图像用于绘制文字
                                    initial_text_width = min(400, img_width // 2)
                                    initial_text_height = 200
                                    text_img = Image.new('RGBA', (initial_text_width, initial_text_height), (0, 0, 0, 0))
                                    text_draw = ImageDraw.Draw(text_img)
                                    
                                    # 加载字体
                                    from PIL import ImageFont
                                    import os
                                    
                                    # 创建text_info对象来存储文本信息
                                    text_info = {
                                        "text": text_info["text"],
                                        "font": text_info["font"],
                                        "color": text_info["color"],
                                        "size": text_info["size"],
                                        "style": text_info["style"],
                                        "effect": text_info["effect"],
                                        "alignment": text_info["alignment"]
                                    }
                                    
                                    # 初始化调试信息列表
                                    font_debug_info = []
                                    font_debug_info.append("Starting high-definition text design")
                                    
                                    # 尝试加载系统字体 - 增强字体处理部分
                                    font = None
                                    try:
                                        # 确保os模块可用
                                        import os
                                        import platform
                                        
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
                                        
                                        # 直接使用完整尺寸的字体大小
                                        render_size = text_info["size"]
                                        font_debug_info.append(f"Trying to load font, size: {render_size}px")
                                        
                                        # 尝试加载每个字体
                                        for font_path in font_paths:
                                            if os.path.exists(font_path):
                                                try:
                                                    font = ImageFont.truetype(font_path, render_size)
                                                    font_debug_info.append(f"Successfully loaded font: {font_path}")
                                                    break
                                                except Exception as font_err:
                                                    font_debug_info.append(f"load font failed: {font_path} - {str(font_err)}")
                                    except Exception as e:
                                        font_debug_info.append(f"font loading process error: {str(e)}")
                                    
                                    # 如果系统字体加载失败，再尝试默认字体
                                    if font is None:
                                        try:
                                            font_debug_info.append("Using PIL default font, which will result in low resolution")
                                            font = ImageFont.load_default()
                                        except Exception as default_err:
                                            font_debug_info.append(f"Default font loading failed: {str(default_err)}")
                                            # 如果连默认字体都失败，创建一个紧急情况文本图像
                                            font_debug_info.append("All fonts loading failed, using emergency solution")
                                    
                                    # 改进的文本渲染方法 - 直接在高分辨率画布上绘制
                                    try:
                                        # 获取T恤图像尺寸
                                        img_width, img_height = new_design.size
                                        
                                        # 创建一个透明的文本图层，大小与T恤相同
                                        text_layer = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
                                        text_draw = ImageDraw.Draw(text_layer)
                                        
                                        # 获取文本边界框以计算尺寸
                                        if font:
                                            # 处理文本换行 - 当文本太长时
                                            max_text_width = int(img_width * 0.7)  # 最大文本宽度为T恤宽度的70%
                                            lines = []
                                            words = text_info["text"].split()
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
                                            
                                            text_width = max_width
                                            text_height = total_height
                                            font_debug_info.append(f"Actual text size: {text_width}x{text_height}px, divided into {len(lines)} lines")
                                        else:
                                            # 估计尺寸
                                            text_width = len(text_info["text"]) * render_size * 0.6
                                            text_height = render_size * 1.2
                                            font_debug_info.append(f"Estimated text size: {text_width}x{text_height}px")
                                        
                                        # 根据对齐方式计算X位置
                                        if text_info["alignment"] == "left":
                                            text_x = int(img_width * 0.2)
                                        elif text_info["alignment"] == "right":
                                            text_x = int(img_width * 0.8 - text_width)
                                        else:  # 居中
                                            text_x = (img_width - text_width) // 2
                                        
                                        # 垂直位置 - 保持在T恤上部
                                        text_y = int(img_height * 0.4 - text_height // 2)
                                        
                                        # 先应用特效
                                        if "style" in text_info:
                                            if "outline" in text_info["style"]:
                                                # 绘制粗轮廓 - 使用更多点以获得更平滑的轮廓
                                                outline_color = "black"
                                                outline_width = max(3, render_size // 20)
                                                
                                                # 8方向轮廓，让描边更均匀
                                                for angle in range(0, 360, 45):
                                                    rad = math.radians(angle)
                                                    offset_x = int(outline_width * math.cos(rad))
                                                    offset_y = int(outline_width * math.sin(rad))
                                                    text_draw.text((text_x + offset_x, text_y + offset_y), 
                                                                  text_info["text"], fill=outline_color, font=font)
                                            
                                            if "shadow" in text_info["style"]:
                                                # 渐变阴影效果
                                                shadow_color = (0, 0, 0, 180)  # 半透明黑色
                                                shadow_offset = max(5, render_size // 15)
                                                blur_radius = shadow_offset // 2
                                                
                                                # 多层阴影创建模糊效果
                                                for i in range(1, blur_radius+1):
                                                    opacity = 180 - (i * 150 // blur_radius)
                                                    current_shadow = (0, 0, 0, opacity)
                                                    offset_i = shadow_offset + i
                                                    text_draw.text((text_x + offset_i, text_y + offset_i), 
                                                                 text_info["text"], fill=current_shadow, font=font)
                                        
                                        # 将文字颜色从十六进制转换为RGBA
                                        text_rgb = tuple(int(text_info["color"].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                                        text_rgba = text_rgb + (255,)  # 完全不透明
                                        
                                        # 绘制主文字 - 考虑多行文本
                                        if "lines" in locals() and len(lines) > 1:
                                            # 多行文本
                                            for i, line in enumerate(lines):
                                                # 计算每行的Y位置
                                                line_y = text_y + i * line_height
                                                # 根据对齐方式重新计算每行X位置
                                                if text_info["alignment"] == "left":
                                                    line_x = text_x
                                                elif text_info["alignment"] == "right":
                                                    line_bbox = text_draw.textbbox((0, 0), line, font=font)
                                                    line_width = line_bbox[2] - line_bbox[0]
                                                    line_x = text_x + (text_width - line_width)
                                                else:  # 居中
                                                    line_bbox = text_draw.textbbox((0, 0), line, font=font)
                                                    line_width = line_bbox[2] - line_bbox[0]
                                                    line_x = text_x + (text_width - line_width) // 2
                                                
                                                # 绘制当前行
                                                text_draw.text((line_x, line_y), line, fill=text_rgba, font=font)
                                        else:
                                            # 单行文本
                                            text_draw.text((text_x, text_y), text_info["text"], fill=text_rgba, font=font)
                                        
                                        # 特殊效果处理
                                        if text_info["effect"] != "none" and text_info["effect"] != "None":
                                            font_debug_info.append(f"Applying special effect: {text_info['effect']}")
                                            if text_info["effect"] == "Gradient":
                                                # 简单实现渐变效果
                                                gradient_layer = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
                                                gradient_draw = ImageDraw.Draw(gradient_layer)
                                                
                                                # 先绘制文字蒙版
                                                gradient_draw.text((text_x, text_y), text_info["text"], 
                                                                 fill=(255, 255, 255, 255), font=font)
                                                
                                                # 创建渐变色彩
                                                from_color = text_rgb
                                                to_color = (255 - text_rgb[0], 255 - text_rgb[1], 255 - text_rgb[2])
                                                
                                                # 将渐变应用到文字
                                                gradient_data = gradient_layer.getdata()
                                                new_data = []
                                                for i, item in enumerate(gradient_data):
                                                    y_pos = i // img_width  # 计算像素的y位置
                                                    if item[3] > 0:  # 如果是文字部分
                                                        # 根据y位置计算颜色混合比例
                                                        ratio = y_pos / text_height
                                                        if ratio > 1: ratio = 1
                                                        
                                                        # 线性混合两种颜色
                                                        r = int(from_color[0] * (1 - ratio) + to_color[0] * ratio)
                                                        g = int(from_color[1] * (1 - ratio) + to_color[1] * ratio)
                                                        b = int(from_color[2] * (1 - ratio) + to_color[2] * ratio)
                                                        new_data.append((r, g, b, item[3]))
                                                    else:
                                                        new_data.append(item)  # 保持透明部分
                                                
                                                gradient_layer.putdata(new_data)
                                                text_layer = gradient_layer
                                        
                                        # 应用文字到设计
                                        new_design.paste(text_layer, (0, 0), text_layer)
                                        
                                        # 保存相关信息
                                        st.session_state.text_position = (text_x, text_y)
                                        st.session_state.text_size_info = {
                                            "font_size": render_size,
                                            "text_width": text_width,
                                            "text_height": text_height
                                        }
                                        
                                        # 应用成功
                                        font_debug_info.append("High-definition text rendering applied successfully")
                                    
                                    except Exception as render_err:
                                        font_debug_info.append(f"High-definition rendering failed: {str(render_err)}")
                                        import traceback
                                        font_debug_info.append(traceback.format_exc())
                                        
                                        # 紧急备用方案 - 创建一个简单文字图像
                                        try:
                                            font_debug_info.append("Using emergency backup rendering method")
                                            # 创建一个白色底的图像
                                            emergency_img = Image.new('RGBA', (img_width//2, img_height//5), (255, 255, 255, 255))
                                            emergency_draw = ImageDraw.Draw(emergency_img)
                                            
                                            # 使用黑色绘制文字，较大字号确保可见
                                            emergency_draw.text((10, 10), text_info["text"], fill="black")
                                            
                                            # 放置在T恤中心位置
                                            paste_x = (img_width - emergency_img.width) // 2
                                            paste_y = (img_height - emergency_img.height) // 2
                                            
                                            new_design.paste(emergency_img, (paste_x, paste_y))
                                            font_debug_info.append("Applied emergency text rendering")
                                        except Exception as emergency_err:
                                            font_debug_info.append(f"Emergency rendering also failed: {str(emergency_err)}")
                                    
                                    # 保存字体加载和渲染信息
                                    st.session_state.font_debug_info = font_debug_info
                                    
                                    # 更新设计和预览
                                    st.session_state.final_design = new_design
                                    st.session_state.current_image = new_design.copy()
                                    
                                    # 保存完整的文字信息
                                    st.session_state.applied_text = {
                                        "text": text_info["text"],
                                        "font": text_info["font"],
                                        "color": text_info["color"],
                                        "size": text_info["size"],
                                        "style": text_info["style"],
                                        "effect": text_info["effect"],
                                        "alignment": text_info["alignment"],
                                        "position": (text_x, text_y),
                                        "use_drawing_method": True  # 标记使用了绘图方法
                                    }
                                    
                                    # 添加详细调试信息
                                    success_msg = f"""
                                    Text applied to design successfully!
                                    Font: {text_info["font"]}
                                    Size: {text_info["size"]}px
                                    Actual width: {text_width}px
                                    Actual height: {text_height}px
                                    Position: ({text_x}, {text_y})
                                    T-shirt size: {img_width} x {img_height}
                                    Rendering method: High-definition rendering
                                    """
                                    
                                    st.success(success_msg)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error applying text: {str(e)}")
                                    import traceback
                                    st.error(traceback.format_exc())
                
                # 重新应用Logo
                if 'applied_logo' in st.session_state and 'selected_preset_logo' in st.session_state:
                    logo_info = st.session_state.applied_logo
                    
                    try:
                        logo_path = st.session_state.selected_preset_logo
                        logo_image = Image.open(logo_path).convert("RGBA")
                        
                        # 获取图像尺寸并使用更大的绘制区域
                        img_width, img_height = st.session_state.final_design.size
                        
                        # 定义更大的T恤前胸区域
                        chest_width = int(img_width * 0.95)  # 几乎整个宽度
                        chest_height = int(img_height * 0.6)  # 更大的高度范围
                        chest_left = (img_width - chest_width) // 2
                        chest_top = int(img_height * 0.2)  # 更高的位置
                        
                        # 调整Logo大小 - 相对于T恤区域而不是小框
                        logo_size_factor = logo_info["size"] / 100
                        logo_width = int(chest_width * logo_size_factor * 0.5)  # 控制最大为区域的一半
                        logo_height = int(logo_width * logo_image.height / logo_image.width)
                        logo_resized = logo_image.resize((logo_width, logo_height), Image.LANCZOS)
                        
                        # 位置映射 - 现在相对于胸前设计区域
                        position_mapping = {
                            "Top-left": (chest_left + 10, chest_top + 10),
                            "Top-center": (chest_left + (chest_width - logo_width) // 2, chest_top + 10),
                            "Top-right": (chest_left + chest_width - logo_width - 10, chest_top + 10),
                            "Center": (chest_left + (chest_width - logo_width) // 2, chest_top + (chest_height - logo_height) // 2),
                            "Bottom-left": (chest_left + 10, chest_top + chest_height - logo_height - 10),
                            "Bottom-center": (chest_left + (chest_width - logo_width) // 2, chest_top + chest_height - logo_height - 10),
                            "Bottom-right": (chest_left + chest_width - logo_width - 10, chest_top + chest_height - logo_height - 10)
                        }
                        
                        logo_x, logo_y = position_mapping.get(logo_info["position"], (chest_left + 10, chest_top + 10))
                        
                        # 设置透明度
                        if logo_info["opacity"] < 100:
                            logo_data = logo_resized.getdata()
                            new_data = []
                            for item in logo_data:
                                r, g, b, a = item
                                new_a = int(a * logo_info["opacity"] / 100)
                                new_data.append((r, g, b, new_a))
                            logo_resized.putdata(new_data)
                        
                        # 粘贴Logo到设计
                        try:
                            final_design = Image.alpha_composite(st.session_state.final_design.convert("RGBA"), logo_resized)
                        except Exception as e:
                            st.warning(f"Logo pasting failed: {e}")
                        
                        # 更新设计
                        st.session_state.final_design = final_design
                        st.session_state.current_image = final_design.copy()
                        
                        # 保存Logo信息用于后续可能的更新
                        st.session_state.applied_logo = {
                            "source": logo_info["source"],
                            "path": st.session_state.get('selected_preset_logo', None),
                            "size": logo_info["size"],
                            "position": logo_info["position"],
                            "opacity": logo_info["opacity"]
                        }
                        
                        st.success("Logo applied to design successfully!")
                        st.rerun()
                    except Exception as e:
                        st.warning(f"Error reapplying logo: {e}")
                
                # 更新已应用的颜色状态
                st.session_state.current_applied_color = st.session_state.shirt_color_hex
        
        # Display current image and get click coordinates
        # 确保current_image存在
        if st.session_state.current_image is not None:
            current_image = st.session_state.current_image
            
            # 确保T恤图像能完整显示
            coordinates = streamlit_image_coordinates(
                current_image,
                key="shirt_image",
                width="100%"
            )
            
            # 添加CSS修复图像显示问题
            st.markdown("""
            <style>
            .stImage img {
                max-width: 100%;
                height: auto;
                object-fit: contain;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Handle selection area logic - simplify to directly move red box
            if coordinates:
                # Update selection box at current mouse position
                current_point = (coordinates["x"], coordinates["y"])
                temp_image, new_pos = draw_selection_box(st.session_state.base_image, current_point)
                st.session_state.current_image = temp_image
                st.session_state.current_box_position = new_pos
                st.rerun()
        else:
            st.warning("Design preview not loaded, please refresh the page and try again.")
        
        # 显示最终设计结果（如果有）
        if st.session_state.final_design is not None:
            st.markdown("### Final result")
            st.image(st.session_state.final_design, use_container_width=True)
            
            # 显示当前颜色
            color_name = {
                "#FFFFFF": "White",
                "#000000": "Black",
                "#FF0000": "Red",
                "#00FF00": "Green",
                "#0000FF": "Blue",
                "#FFFF00": "Yellow",
                "#FF00FF": "Magenta",
                "#00FFFF": "Cyan",
                "#C0C0C0": "Silver",
                "#808080": "Gray"
            }.get(st.session_state.shirt_color_hex.upper(), "Custom")
            st.markdown(f"**Color:** {color_name} ({st.session_state.shirt_color_hex})")
            
            # 显示面料信息
            fabric_type = st.session_state.fabric_type if 'fabric_type' in st.session_state else "Cotton"
            st.markdown(f"**Fabric:** {fabric_type}")
            
            # 显示调试信息
            if st.checkbox("Show debug information", value=True):
                st.write("---")
                st.subheader("Debug information")
                
                # 显示图像尺寸信息
                if hasattr(st.session_state, 'tshirt_size'):
                    st.write(f"T-shirt image size: {st.session_state.tshirt_size[0]} x {st.session_state.tshirt_size[1]} pixels")
                
                # 显示文字信息
                if hasattr(st.session_state, 'text_size_info'):
                    text_info = st.session_state.text_size_info
                    st.write(f"Font size: {text_info['font_size']} pixels")
                    st.write(f"Text width: {text_info['text_width']} pixels")
                    st.write(f"Text height: {text_info['text_height']} pixels")
                
                # 显示位置信息
                if hasattr(st.session_state, 'text_position'):
                    st.write(f"Text position: {st.session_state.text_position}")
                
                # 显示设计区域信息
                if hasattr(st.session_state, 'design_area'):
                    design_area = st.session_state.design_area
                    st.write(f"Design area: Top-left({design_area[0]}, {design_area[1]}), width({design_area[2]}, {design_area[3]})")
                
                # 显示字体加载路径
                if hasattr(st.session_state, 'loaded_font_path'):
                    st.write(f"Loaded font path: {st.session_state.loaded_font_path}")
                
                # 显示字体加载状态
                if hasattr(st.session_state, 'using_fallback_text'):
                    if st.session_state.using_fallback_text:
                        st.error("Font loading failed, using fallback rendering method")
                    else:
                        st.success("Font loaded successfully")
                
                # 显示详细的字体加载信息（如果存在）
                if hasattr(st.session_state, 'font_debug_info'):
                    with st.expander("Font loading detailed information"):
                        for info in st.session_state.font_debug_info:
                            st.write(f"- {info}")
            
            # 添加清空设计按钮
            if st.button("🗑️ Clear all designs", key="clear_designs"):
                # 清空所有设计相关的状态变量
                st.session_state.generated_design = None
                st.session_state.applied_text = None
                st.session_state.applied_logo = None
                st.session_state.generated_logo = None
                st.session_state.logo_auto_generated = False
                st.session_state.show_generated_logo = False
                
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
            # 添加用户偏好输入
            user_preference = st.text_input("Describe your preferred style or usage", placeholder="For example: sports style, business场合, casual daily, etc.")
            
            col_pref1, col_pref2 = st.columns([1, 1])
            with col_pref1:
                # 添加预设风格选择
                preset_styles = ["", "Fashion casual", "Business formal", "Sports style", "Rock and roll", "Japanese anime", "Artistic retro", "American street"]
                selected_preset = st.selectbox("Or select a preset style:", preset_styles)
                if selected_preset and not user_preference:
                    user_preference = selected_preset
            
            with col_pref2:
                # 添加获取建议按钮
                if st.button("Get personalized AI suggestions", key="get_ai_advice"):
                    with st.spinner("Generating personalized design suggestions..."):
                        suggestions = get_ai_design_suggestions(user_preference)
                        st.session_state.ai_suggestions = suggestions
            
            # 显示AI建议
            if st.session_state.ai_suggestions:
                # 添加格式化的建议显示
                st.markdown("""
                <style>
                .suggestion-container {
                    background-color: #f8f9fa;
                    border-left: 4px solid #4CAF50;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 0 5px 5px 0;
                }
                .suggestion-section {
                    margin-bottom: 12px;
                    font-weight: 500;
                }
                .suggestion-item {
                    margin-left: 15px;
                    margin-bottom: 8px;
                }
                .color-name {
                    font-weight: 500;
                }
                .color-code {
                    font-family: monospace;
                    background-color: #f1f1f1;
                    padding: 2px 4px;
                    border-radius: 3px;
                }
                .suggested-text {
                    cursor: pointer;
                    color: #0066cc;
                    transition: all 0.2s;
                }
                .suggested-text:hover {
                    background-color: #e6f2ff;
                    text-decoration: underline;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(st.session_state.ai_suggestions, unsafe_allow_html=True)
                
                # 添加应用建议的部分
                st.markdown("---")
                st.markdown("#### Apply AI suggestions")
                
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
                
                st.markdown("##### Apply recommended colors")
                
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
                st.markdown("##### Fabric Texture")
                if 'fabric_type' not in st.session_state:
                    st.session_state.fabric_type = "Cotton"  # 默认面料类型
                
                # 如果有AI推荐的面料，则显示它们
                if 'ai_suggested_fabrics' in st.session_state and st.session_state.ai_suggested_fabrics:
                    st.markdown("**AI Recommended Fabrics:**")
                    
                    # 创建面料推荐显示
                    fabric_matches = st.session_state.ai_suggested_fabrics
                    fabric_cols = st.columns(min(2, len(fabric_matches)))
                    
                    for i, (fabric_name, fabric_desc) in enumerate(fabric_matches.items()):
                        with fabric_cols[i % 2]:
                            # 显示简短描述
                            short_desc = fabric_desc[:100] + "..." if len(fabric_desc) > 100 else fabric_desc
                            
                            st.markdown(f"**{fabric_name}**")
                            st.markdown(f"*{short_desc}*")
                            
                            if st.button(f"Use {fabric_name}", key=f"fabric_{i}"):
                                # 更新面料类型
                                st.session_state.fabric_type = fabric_name
                                
                                # 应用面料纹理
                                if st.session_state.original_base_image is not None:
                                    try:
                                        # 应用纹理
                                        new_colored_image = change_shirt_color(
                                            st.session_state.original_base_image,
                                            st.session_state.shirt_color_hex,
                                            apply_texture=True,
                                            fabric_type=fabric_name
                                        )
                                        st.session_state.base_image = new_colored_image
                                        
                                        # 更新当前图像
                                        new_image, _ = draw_selection_box(new_colored_image, st.session_state.current_box_position)
                                        st.session_state.current_image = new_image
                                        
                                        # 如果有最终设计，也需要更新
                                        if st.session_state.final_design is not None:
                                            st.session_state.final_design = new_colored_image.copy()
                                        
                                        st.success(f"Applied {fabric_name} texture")
                                        st.rerun()
                                    except Exception as e:
                                        st.warning(f"Error applying fabric texture: {e}")
                
                st.markdown("---")
                st.markdown("**All Available Fabrics:**")
                # 面料选择
                fabric_options = ["Cotton", "Polyester", "Cotton-Polyester Blend", "Jersey", "Linen", "Bamboo"]
                fabric_type = st.selectbox("Fabric type:", fabric_options,
                                        index=fabric_options.index(st.session_state.fabric_type)
                                        if st.session_state.fabric_type in fabric_options else 0)
                
                # 应用面料纹理按钮
                texture_col1, texture_col2 = st.columns([3, 1])
                with texture_col1:
                    # 显示面料类型说明
                    fabric_descriptions = {
                        "Cotton": "Soft natural fiber with good breathability",
                        "Polyester": "Durable synthetic fabric that resists wrinkles",
                        "Cotton-Polyester Blend": "Combines comfort and durability",
                        "Jersey": "Stretchy knit fabric with good drape",
                        "Linen": "Light natural fabric with excellent cooling properties",
                        "Bamboo": "Sustainable fabric with silky soft texture"
                    }
                    st.markdown(f"*{fabric_descriptions.get(fabric_type, '')}*")
                
                with texture_col2:
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
                
                # 文字建议应用
                st.markdown("##### Apply recommended text")
                
                # 显示解析的推荐文字，点击直接填充
                if 'ai_suggested_texts' in st.session_state and st.session_state.ai_suggested_texts:
                    st.markdown("**Click the recommended text below to apply quickly:**")
                    suggested_texts_container = st.container()
                    with suggested_texts_container:
                        text_buttons = st.columns(min(2, len(st.session_state.ai_suggested_texts)))
                        
                        for i, text in enumerate(st.session_state.ai_suggested_texts):
                            with text_buttons[i % 2]:
                                # 修改按钮实现方式，避免直接设置会话状态
                                if st.button(f'"{text}"', key=f"text_btn_{i}"):
                                    # 创建一个临时状态变量
                                    st.session_state.temp_text_selection = text
                                    st.rerun()
                
                # 文字选项 - 使用高复杂度方案的全部功能
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
                    
                    text_content = st.text_input("Input or copy the recommended text by AI", default_input, key="ai_text_suggestion")
                
                with text_col2:
                    text_color = st.color_picker("Text color:", "#000000", key="ai_text_color")
                
                # 字体选择 - 扩展为高复杂度方案的选项
                font_options = ["Arial", "Times New Roman", "Courier", "Verdana", "Georgia", "Script", "Impact"]
                font_family = st.selectbox("Font series:", font_options, key="ai_font_selection")
                
                # 添加文字样式选项
                text_style = st.multiselect("Text style:", ["Bold", "Italic", "Underline", "Shadow", "Outline"], default=["Bold"])
                
                # 添加动态文字大小滑块 - 增加最大值
                text_size = st.slider("Text size:", 20, 400, 39, key="ai_text_size")
                
                # 添加文字效果选项
                text_effect = st.selectbox("Text effect:", ["None", "Bent", "Arch", "Wave", "3D", "Gradient"])
                
                # 添加对齐方式选项
                alignment = st.radio("Alignment:", ["Left", "Center", "Right"], horizontal=True, index=1)
                
                # 修改预览部分，添加样式效果
                if text_content:
                    # 构建样式字符串
                    style_str = ""
                    if "粗体" in text_style:
                        style_str += "font-weight: bold; "
                    if "斜体" in text_style:
                        style_str += "font-style: italic; "
                    if "下划线" in text_style:
                        style_str += "text-decoration: underline; "
                    if "阴影" in text_style:
                        style_str += "text-shadow: 2px 2px 4px rgba(0,0,0,0.5); "
                    if "轮廓" in text_style:
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
                    
                # 修改应用文字到设计部分的代码，完全重写文字应用逻辑
                if st.button("Apply text to design", key="apply_ai_text"):
                    if not text_content.strip():
                        st.warning("请输入文字内容！")
                    else:
                        with st.spinner("正在应用文字设计..."):
                            try:
                                # 导入必要的模块
                                from PIL import ImageFont
                                
                                # 获取当前图像
                                if st.session_state.final_design is not None:
                                    new_design = st.session_state.final_design.copy()
                                else:
                                    new_design = st.session_state.base_image.copy()
                                
                                # 确保图像是RGBA模式
                                new_design = new_design.convert('RGBA')
                                
                                # 创建文字图层
                                text_layer = Image.new('RGBA', new_design.size, (0, 0, 0, 0))
                                text_draw = ImageDraw.Draw(text_layer)
                                
                                # 计算文字位置
                                img_width, img_height = new_design.size
                                text_x = img_width // 2  # 居中
                                text_y = img_height // 3  # 在上部1/3处
                                
                                # 设置字体大小
                                font_size = text_size
                                
                                # 尝试加载系统字体
                                try:
                                    import os
                                    font_path = "C:/Windows/Fonts/arial.ttf"  # Windows系统字体路径
                                    if os.path.exists(font_path):
                                        font = ImageFont.truetype(font_path, font_size)
                                    else:
                                        font = ImageFont.load_default()
                                except Exception:
                                    font = ImageFont.load_default()
                                
                                # 转换颜色为RGBA
                                text_rgb = tuple(int(text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                                text_rgba = text_rgb + (255,)  # 完全不透明
                                
                                # 获取文字边界框
                                bbox = text_draw.textbbox((text_x, text_y), text_content, font=font, anchor="mm")
                                text_width = bbox[2] - bbox[0]
                                text_height = bbox[3] - bbox[1]
                                
                                # 根据对齐方式调整位置
                                if alignment == "Left":
                                    text_x = int(img_width * 0.2)
                                elif alignment == "Right":
                                    text_x = int(img_width * 0.8)
                                # Center保持不变
                                
                                # 应用文字样式
                                if "Shadow" in text_style:
                                    # 绘制阴影
                                    shadow_offset = 3
                                    text_draw.text((text_x + shadow_offset, text_y + shadow_offset), 
                                                 text_content, font=font, fill=(0, 0, 0, 128), anchor="mm")
                                
                                if "Outline" in text_style:
                                    # 绘制轮廓
                                    outline_color = (0, 0, 0, 255)
                                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                                        text_draw.text((text_x + dx, text_y + dy), 
                                                     text_content, font=font, fill=outline_color, anchor="mm")
                                
                                # 绘制主文字
                                text_draw.text((text_x, text_y), text_content, 
                                             font=font, fill=text_rgba, anchor="mm")
                                
                                # 合并图层
                                new_design = Image.alpha_composite(new_design, text_layer)
                                
                                # 更新设计
                                st.session_state.final_design = new_design
                                st.session_state.current_image = new_design.copy()
                                
                                # 保存文字信息
                                st.session_state.applied_text = {
                                    "text": text_content,
                                    "font": font_family,
                                    "color": text_color,
                                    "size": text_size,
                                    "style": text_style,
                                    "effect": text_effect,
                                    "alignment": alignment,
                                    "position": (text_x, text_y)
                                }
                                
                                st.success("文字已成功应用到设计上！")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"应用文字时出错: {str(e)}")
                                import traceback
                                st.error(traceback.format_exc())
                
                # 添加Logo选择功能
                st.markdown("##### Apply Logo")

                # 显示自动生成的Logo
                if hasattr(st.session_state, 'generated_logo') and hasattr(st.session_state, 'logo_auto_generated') and st.session_state.logo_auto_generated:
                    logo_auto_col1, logo_auto_col2 = st.columns([3, 2])
                    
                    with logo_auto_col1:
                        # 显示Logo
                        preview_width = 200
                        preview_height = int(preview_width * st.session_state.generated_logo.height / st.session_state.generated_logo.width)
                        st.image(st.session_state.generated_logo, caption="AI generated Logo", width=preview_width)
                    
                    with logo_auto_col2:
                        st.success("Logo generated automatically based on AI suggestions")
                        st.markdown(f"**Prompt**：{st.session_state.logo_prompt}")
                        
                        # 直接提供应用Logo的按钮
                        if st.button("Apply this Logo to design directly", key="apply_auto_logo"):
                            with st.spinner("Applying Logo to design..."):
                                try:
                                    # 获取当前图像
                                    if st.session_state.final_design is not None:
                                        new_design = st.session_state.final_design.copy()
                                    else:
                                        new_design = st.session_state.base_image.copy()
                                    
                                    # 获取图像尺寸并使用更大的绘制区域
                                    img_width, img_height = new_design.size
                                    
                                    # 定义更大的T恤前胸区域
                                    chest_width = int(img_width * 0.95)  # 几乎整个宽度
                                    chest_height = int(img_height * 0.6)  # 更大的高度范围
                                    chest_left = (img_width - chest_width) // 2
                                    chest_top = int(img_height * 0.2)  # 更高的位置
                                    
                                    # 使用默认设置
                                    logo_size = 40  # 默认40%大小
                                    logo_position = "Center"  # 默认居中
                                    logo_opacity = 100  # 默认100%不透明
                                    
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
                                    
                                    # 粘贴Logo到设计
                                    new_design.paste(logo_resized, (logo_x, logo_y), logo_resized)
                                    
                                    # 更新设计
                                    st.session_state.final_design = new_design
                                    st.session_state.current_image = new_design.copy()
                                    
                                    # 保存Logo信息
                                    st.session_state.applied_logo = {
                                        "prompt": st.session_state.logo_prompt,
                                        "size": logo_size,
                                        "position": logo_position,
                                        "opacity": logo_opacity
                                    }
                                    
                                    st.success("Logo applied to design successfully!")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"Error applying Logo: {str(e)}")
                                    import traceback
                                    st.error(traceback.format_exc())

                # Logo生成选项
                logo_col1, logo_col2 = st.columns([2, 1])

                with logo_col1:
                    # 根据AI建议的Logo元素自动填充初始提示词
                    initial_logo_prompt = ""
                    if hasattr(st.session_state, 'ai_suggested_logos') and st.session_state.ai_suggested_logos:
                        # 使用第一个推荐的Logo描述
                        initial_logo_prompt = st.session_state.ai_suggested_logos[0]
                    
                    logo_prompt = st.text_input("Describe the Logo style you want", 
                                               value=initial_logo_prompt,
                                               placeholder="For example: A simple modern mountain logo, using blue and white")

                with logo_col2:
                    # 修改自动生成状态显示 - 移除这部分提示
                    # if hasattr(st.session_state, 'logo_auto_generated') and st.session_state.logo_auto_generated:
                    #    st.info("您可以修改提示词重新生成Logo")
                    
                    if st.button("Generate Logo", key="generate_logo"):
                        if not logo_prompt:
                            st.warning("Please enter a Logo description")
                        else:
                            with st.spinner("Generating Logo..."):
                                try:
                                    # 构建完整的提示词
                                    full_prompt = f"Create a T-shirt Logo design: {logo_prompt}. Requirements: 1. Use a simple design 2. Suitable for T-shirt printing 3. Background transparent 4. Clear and recognizable图案清晰可识别"
                                    
                                    # 调用DALL-E生成图像
                                    logo_image = generate_vector_image(full_prompt)
                                    
                                    if logo_image:
                                        # 保存生成的Logo
                                        st.session_state.generated_logo = logo_image
                                        # 保存Logo提示词
                                        st.session_state.logo_prompt = logo_prompt
                                        # 标记为用户手动生成的Logo
                                        st.session_state.logo_auto_generated = False
                                        st.success("Logo generated successfully!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error generating Logo: {str(e)}")

                # 如果有其他AI建议的Logo元素，显示切换选项
                if hasattr(st.session_state, 'ai_suggested_logos') and len(st.session_state.ai_suggested_logos) > 1:
                    # 修改显示逻辑，即使已经生成了Logo也显示其他建议
                    st.markdown("**Other Logo suggestions from AI:**")
                    for i, logo_desc in enumerate(st.session_state.ai_suggested_logos[1:], 1):
                        if st.button(f"Use suggestion {i}: {logo_desc[:50]}...", key=f"use_logo_suggestion_{i}"):
                            with st.spinner("Generating Logo..."):
                                try:
                                    # 构建完整的提示词
                                    full_prompt = f"Create a Logo design: {logo_desc}. Requirements: 1. Use a simple design 2. Suitable for printing 3. Background transparent 4. Clear and recognizable图案清晰可识别"
                                    
                                    # 调用DALL-E生成图像
                                    logo_image = generate_vector_image(full_prompt)
                                    
                                    if logo_image:
                                        # 保存生成的Logo
                                        st.session_state.generated_logo = logo_image
                                        # 保存Logo提示词
                                        st.session_state.logo_prompt = logo_desc
                                        # 标记为用户选择的Logo
                                        st.session_state.logo_auto_generated = False
                                        st.success("Logo generated successfully!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error generating Logo: {str(e)}")

                # If there is a generated Logo, display the Logo settings options
                if hasattr(st.session_state, 'generated_logo'):
                    st.markdown("#### Logo settings")
                    
                    # 显示已生成的Logo提示词和预览
                    logo_preview_col, logo_regen_col = st.columns([3, 2])
                    
                    with logo_preview_col:
                        # 显示生成的Logo预览
                        preview_width = 200
                        preview_height = int(preview_width * st.session_state.generated_logo.height / st.session_state.generated_logo.width)
                        st.image(st.session_state.generated_logo, caption="Generated Logo", width=preview_width)
                    
                    with logo_regen_col:
                        # 显示当前使用的提示词和生成方式
                        if hasattr(st.session_state, 'logo_auto_generated') and st.session_state.logo_auto_generated:
                            st.markdown(f"**Current prompt**：{st.session_state.logo_prompt if hasattr(st.session_state, 'logo_prompt') else '未指定'} (Auto generated)")
                        else:
                            st.markdown(f"**Current prompt**：{st.session_state.logo_prompt if hasattr(st.session_state, 'logo_prompt') else '未指定'}")
                        
                        # 添加重新生成选项
                        new_logo_prompt = st.text_input("Enter a new Logo description to regenerate", placeholder="Describe the new Logo style you want", key="new_logo_prompt")
                        
                        if st.button("Regenerate Logo", key="regenerate_logo"):
                            if not new_logo_prompt:
                                st.warning("Please enter a new Logo description")
                            else:
                                with st.spinner("Regenerating Logo..."):
                                    try:
                                        # 构建完整的提示词
                                        full_prompt = f"Create a Logo design: {new_logo_prompt}. Requirements: 1. Use a simple design 2. Suitable for printing 3. Background transparent 4. Clear and recognizable图案清晰可识别"
                                        
                                        # 调用DALL-E生成图像
                                        logo_image = generate_vector_image(full_prompt)
                                        
                                        if logo_image:
                                            # 保存生成的Logo
                                            st.session_state.generated_logo = logo_image
                                            # 更新Logo提示词
                                            st.session_state.logo_prompt = new_logo_prompt
                                            # 标记为用户手动生成的Logo
                                            st.session_state.logo_auto_generated = False
                                            st.success("Logo regenerated successfully!")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Error regenerating Logo: {str(e)}")
                    
                    # Logo大小
                    logo_size = st.slider("Logo size:", 10, 100, 40, format="%d%%", key="ai_logo_size")
                    
                    # Logo位置
                    logo_position = st.radio("Position:", 
                        ["Top-left", "Top-center", "Top-right", "Center", "Bottom-left", "Bottom-center", "Bottom-right"], 
                        index=3, horizontal=True, key="ai_logo_position")
                    
                    # Logo透明度
                    logo_opacity = st.slider("Logo opacity:", 10, 100, 100, 5, format="%d%%", key="ai_logo_opacity")
                    
                    # 应用Logo按钮
                    if st.button("Apply Logo to design", key="apply_ai_logo"):
                        with st.spinner("Applying Logo to design..."):
                            try:
                                # 获取当前图像
                                if st.session_state.final_design is not None:
                                    new_design = st.session_state.final_design.copy()
                                else:
                                    new_design = st.session_state.base_image.copy()
                                
                                # 获取图像尺寸并使用更大的绘制区域
                                img_width, img_height = new_design.size
                                
                                # 定义更大的T恤前胸区域
                                chest_width = int(img_width * 0.95)  # 几乎整个宽度
                                chest_height = int(img_height * 0.6)  # 更大的高度范围
                                chest_left = (img_width - chest_width) // 2
                                chest_top = int(img_height * 0.2)  # 更高的位置
                                
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
                                new_design.paste(logo_resized, (logo_x, logo_y), logo_resized)
                                
                                # 更新设计
                                st.session_state.final_design = new_design
                                st.session_state.current_image = new_design.copy()
                                
                                # 保存Logo信息
                                st.session_state.applied_logo = {
                                    "prompt": st.session_state.logo_prompt,
                                    "size": logo_size,
                                    "position": logo_position,
                                    "opacity": logo_opacity
                                }
                                
                                # 添加详细调试信息
                                success_msg = f"""
                                Logo applied successfully!
                                Prompt: {st.session_state.logo_prompt}
                                Size: {logo_size}%
                                Actual width: {logo_width}px
                                Actual height: {logo_height}px
                                Position: {logo_position} ({logo_x}, {logo_y})
                                Opacity: {logo_opacity}%
                                T-shirt size: {img_width} x {img_height}
                                """
                                
                                st.success(success_msg)
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Apply Logo error: {str(e)}")
                                import traceback
                                st.error(traceback.format_exc())
            else:
                # 显示欢迎信息
                st.markdown("""
                <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1e88e5;">
                <h4 style="color: #1e88e5; margin-top: 0;">👋 Welcome to the AI design assistant</h4>
                <p>Describe your preferred style or T-shirt purpose, the AI assistant will provide personalized design suggestions, including:</p>
                <ul>
                    <li>Recommended T-shirt colors for your style</li>
                    <li>Text content and font style suggestions</li>
                    <li>Logo selection and design element recommendations</li>
                </ul>
                <p>Click the "Get personalized AI suggestions" button to start!</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Return to main interface button - modified here
    if st.button("Back to main page"):
        # Clear all design-related states
        st.session_state.base_image = None
        st.session_state.current_image = None
        st.session_state.current_box_position = None
        st.session_state.generated_design = None
        st.session_state.final_design = None
        st.session_state.applied_text = None
        st.session_state.applied_logo = None
        # Only change page state, retain user info and experiment group
        st.session_state.page = "welcome"
        st.rerun() 
