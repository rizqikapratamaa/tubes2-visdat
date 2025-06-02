import streamlit as st
import data_loader
import config

def display_key_findings():
    st.markdown(
        f"<h3 style='text-align: center; color: #E2E8F0; padding-top: 10px;'>Key Findings</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='
            padding: 40px 15%;
            margin-bottom: 20px;
        '>
            <ul style='
                color: #E0E7FF;
                font-size: 16px;
                line-height: 1.8;
                padding-left: 20px;
                margin: 0;
            '>
                <li style='margin-bottom: 15px;'>
                    China’s lead over the United States in international trade relationships has only widened since the last US–China trade war of 2018–19.
                </li>
                <li style='margin-bottom: 15px;'>
                    Around 70 per cent of economies trade more with China than they do with America, and more than half of all economies now trade twice as much with China compared to the United States.
                </li>
                <li>
                    China’s global trade relationships remain deeply unbalanced, with a trillion-dollar surge in China’s merchandise exports since the pandemic, while its imports have not kept pace.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><hr style='margin-top: 0.5rem; margin-bottom: 0.5rem;'><br>", unsafe_allow_html=True)

def display_authors():
    qika_base64 = data_loader.image_to_base64('assets/qika.jpg')
    yasmin_base64 = data_loader.image_to_base64('assets/yasmin.jpg')

    st.markdown(
        f"<h3 style='text-align: center; color: #E2E8F0; padding-top: 10px; margin-bottom: 20px;'>About the Authors</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style='
            padding: 40px 10%;
            margin-bottom: 20px;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        '>
            <div style='
                display: flex;
                justify-content: center; 
                align-items: center;
                gap: 40px;
                flex-wrap: wrap;
            '>
                <!-- Author 1 -->
                <div style='
                    display: flex;
                    align-items: center;
                    flex: 1;
                    min-width: 300px;
                    max-width: 400px; 
                    gap: 30px;
                '>
                    <img src='data:image/jpeg;base64,{qika_base64}' style='
                        width: 80px;
                        height: 80px;
                        border-radius: 50%;
                        object-fit: cover;
                    '/>
                    <div style='padding: 5px 0;'> 
                        <h4 style='
                            color: #FFFFFF;
                            font-size: 18px;
                            font-weight: bold;
                            margin-bottom: 5px;
                        '>
                            Rizqika Mulia Pratama
                        </h4>
                        <p style='
                            color: #E0E7FF;
                            font-size: 14px;
                            line-height: 1.5;
                            margin: 0;
                        '>
                            13522126
                        </p>
                    </div>
                </div>
                <!-- Author 2 -->
                <div style='
                    display: flex;
                    align-items: center;
                    flex: 1;
                    min-width: 300px;
                    max-width: 400px;
                    gap: 30px; 
                '>
                    <img src='data:image/jpeg;base64,{yasmin_base64}' style='
                        width: 80px;
                        height: 80px;
                        border-radius: 50%;
                        object-fit: cover;
                    '/>
                    <div style='padding: 5px 0;'>
                        <h4 style='
                            color: #FFFFFF;
                            font-size: 18px;
                            font-weight: bold;
                            margin-bottom: 5px;
                        '>
                            Yasmin Farisah Salma
                        </h4>
                        <p style='
                            color: #E0E7FF;
                            font-size: 14px;
                            line-height: 1.5;
                            margin: 0;
                        '>
                            13522140
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )