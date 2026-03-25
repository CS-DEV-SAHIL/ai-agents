import streamlit as st
from blogdon.crew import Blogdon
from datetime import datetime
import os
import re

def main():
    st.set_page_config(page_title="BlogDon - AI Blog Generator", page_icon="📝", layout="wide")

    st.title("📝 BlogDon: AI-Powered Blog Generator")
    st.markdown("""
    Generate custom-length, plain text blog posts in simple English.
    """)

    with st.sidebar:
        st.header("Settings")
        st.info("Ensure your `.env` file is configured with your API keys.")
        if st.button("Clear Cache"):
            st.cache_data.clear()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Input Parameters")
        topic = st.text_input("Blog Topic", placeholder="e.g., The Future of AI in Healthcare")
        keywords_str = st.text_area("Keywords (comma separated)", placeholder="e.g., AI, Healthcare, Innovation, Future")
        
        blog_length = st.selectbox(
            "Blog Length",
            options=["Short (~300-500 words)", "Medium (~700-1000 words)", "Long (~1500+ words)"],
            index=1
        )
        
        generate_button = st.button("🚀 Generate Blog Post", use_container_width=True)

    if generate_button:
        if not topic:
            st.error("Please provide a topic.")
        else:
            keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
            
            inputs = {
                'topic': topic,
                'keywords': keywords,
                'blog_length': blog_length.split(" ")[0],
                'current_year': str(datetime.now().year)
            }

            with st.status("🤖 AI Agents at work...", expanded=True) as status:
                try:
                    st.write("🏃‍♂️ Starting the Crew...")
                    result = Blogdon().crew().kickoff(inputs=inputs)
                    
                    status.update(label="✅ Blog Generated Successfully!", state="complete", expanded=False)
                    
                    raw_content = result.raw
                    
                    # Extract Humanize Score if present
                    score_match = re.search(r"HUMANIZE_SCORE:\s*(\d+)", raw_content)
                    score = score_match.group(1) if score_match else "N/A"
                    
                    # Clean the content - remove the score line from the displayed text
                    clean_content = re.sub(r"HUMANIZE_SCORE:\s*\d+", "", raw_content).strip()
                    
                    with col2:
                        st.subheader("Final Output")
                        
                        if score != "N/A":
                            st.metric(label="Humanize English Score", value=f"{score}/10")
                        
                        st.text_area("Blog Content", value=clean_content, height=500)
                        
                        st.download_button(
                            label="📥 Download Blog Post (Text)",
                            data=clean_content,
                            file_name=f"{topic.lower().replace(' ', '_')}_blog.txt",
                            mime="text/plain"
                        )
                        
                        if os.path.exists("final_blog_post.txt"):
                            st.success("Saved to local file: `final_blog_post.txt`")

                except Exception as e:
                    if "quota" in str(e).lower():
                        st.error("Rate limit reached (Gemini API). Please wait a minute and try again.")
                    else:
                        st.error(f"An error occurred: {e}")
                    status.update(label="❌ Generation Failed", state="error")

if __name__ == "__main__":
    main()
