import streamlit as st
from PIL import Image
from utils import load_model, predict_ingredients, load_recipes, recommend_recipes, get_full_recipe

st.set_page_config(page_title="Ingredient Scanner", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Soft green background for sidebar */
        section[data-testid="stSidebar"] {
            background-color: #e6f4ea;
            padding: 20px;
        }

        /* Title style */
        .title-text {
            color: #4caf50; /* soft green */
            font-size: 2.8em;
            font-weight: bold;
        }

        /* Ingredient tag style */
        .ingredient-box {
            display: inline-block;
            background-color: #d4edda;
            border-radius: 8px;
            padding: 6px 12px;
            margin: 5px 6px;
            font-size: 14px;
            color: #2e7d32;
        }

        /* Recipe card style */
        .recipe-card {
            border: 1px solid #d0e6d5;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: #f8fcf9;
            transition: 0.3s ease;
        }

        .recipe-card:hover {
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
        }

        .full-recipe-title {
            font-size: 24px;
            color: #388e3c;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Page Setup ---
st.markdown('<div class="title-text">🥦 Cuiscan: AI Powered Recipe Recommendation 🥦</div>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("Welcome to Cuiscan!")
    st.write("A short form of Quick and Scan, just like how it works.")
    st.subheader("About Us")
    st.markdown("""
    🧡 Created by Aliaa Othman  
    🧡 Powered by YOLOv8 Ultralytics  
    🧡 Recipes by Che Nom  
    """)
    st.subheader("How To Use?")
    st.markdown("""
    1. Upload a well-lit image of your ingredients  
    2. Click **Scan Ingredients**  
    3. Browse and click a recipe to view the full instructions  
    """)

# --- Session State ---
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

# --- Upload Section ---
st.subheader('📷 Upload an image of ingredients')
uploaded_file = st.file_uploader(label="Choose an image...", type=["jpg", "png", "jpeg"])

# --- Display Image and Scan ---
if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image

    st.image(image, caption="Uploaded Image", width=300)
    if st.button("🔍 Scan Ingredients"):
        model = load_model("yolov8_model/yolov8n_lr001_bsz32.pt")
        ingredients = predict_ingredients(model, image)
        st.session_state.ingredients = ingredients
        st.session_state.selected_recipe = None

# --- Recognized Ingredients Display ---
if st.session_state.ingredients:
    st.subheader("🧾 Recognized Ingredients")
    ingredient_tags = "".join([f"<span class='ingredient-box'>{i}</span>" for i in st.session_state.ingredients])
    st.markdown(ingredient_tags, unsafe_allow_html=True)

    # --- Recommend Recipes ---
    all_recipes = load_recipes()
    matches = recommend_recipes(st.session_state.ingredients, all_recipes)

    if not matches:
        st.warning("No matching recipes found with these ingredients.")
    else:
        st.subheader("🍽️ Recommended Recipes")
        for i, recipe in enumerate(matches):
            with st.container():
                st.markdown(f"**{recipe['title']}**")
                
                with st.expander("📖 View Full Recipe"):
                    st.session_state.selected_recipe = recipe['title']
                    try:
                        instructions, recipe_img = get_full_recipe(recipe['title'])
                        st.image(recipe_img, use_container_width=True)
                        st.markdown(instructions)
                    except Exception as e:
                        st.error(f"Error loading recipe: {str(e)}")
