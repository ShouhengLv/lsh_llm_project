import streamlit as st
from PIL import Image
import io
from llm_interface import call_llm_stream_multimodal
from schema.validator import full_output_validate,full_input_validate  # 导入输入内容校验


st.set_page_config(page_title="智能问答机器人", page_icon="🤖")

st.title("🤖 智能问答机器人（LLM Demo）")
st.markdown("通过接入deepseek-R1，实现交互问答，支持 temperature 控制。")

# （1）文本输入
text_input = st.text_area("请输入你的问题（必填）：", height=100, key="input")

# （2）图像输入
uploaded_file = st.file_uploader("上传图片（选填）", type=["png", "jpg", "jpeg"])
image_bytes = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的图片", use_container_width=True)
    image_bytes = uploaded_file.read()

# Temperature 滑动条
temperature = st.slider("temperature（输出多样性）", 0.0, 2.0, 0.7, 0.1)

# 生成按钮
if st.button("发送给模型"):
    
    #读入文本
    if not text_input.strip():
        st.warning("请输入内容！")
        
    else:
        # Step 2: JSON Schema 输入结构校验
        try:
            full_input_validate({"prompt": text_input, "temperature": temperature})

        except ValueError as ve:
            st.error(f"❌ 输入校验失败：{ve}")
            
        else:
            with st.spinner("正在生成回答，请稍候..."):
                try:
                    placeholder = st.empty()  # 占位，后面动态更新文本
                    response_text = ""
                    for chunk in call_llm_stream_multimodal(text_input, image_bytes, temperature=temperature):
                        #st.write(f"收到 chunk：{chunk}") 
                        response_text += chunk
                        placeholder.markdown(response_text + "▌")  # 加个光标感
                    placeholder.markdown(response_text)  # 结束后去掉光标
                    
                    #由于输出是流式输出，为了前端交互的可观赏性，所以不对输出进行结构化校验
                        
                except Exception as e:
                    st.error(f"❌ 出错: {str(e)}")