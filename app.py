import streamlit as st

from products import products

# ==========================================
# CUSTOM SHOPAI DASHBOARD STYLE
# ==========================================

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */

    .stApp {
        background: linear-gradient(
            135deg,
            #f4f7ff,
            #eef2ff
        );
    }


    /* MAIN TITLE */

    h1 {
        color: #312e81;
        font-weight: 800;
    }


    /* SECTION HEADERS */

    h2 {
        color: #1e3a8a;
        padding: 10px;
        border-left: 6px solid #7c3aed;
    }


    /* SUBHEADERS */

    h3 {
        color: #4338ca;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #312e81,
            #4c1d95
        );
    }


    section[data-testid="stSidebar"] * {
        color: white;
    }


    /* BUTTONS */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: none;
    }


    /* INPUT BOXES */

    input,
    textarea {
        border-radius: 8px !important;
    }


    /* METRIC BOXES */

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(
            0,
            0,
            0,
            0.08
        );
        border-left: 5px solid #6366f1;
    }

    /* ==========================================
   COLORFUL DASHBOARD METRICS
========================================== */

div[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #ffffff,
        #eef2ff
    );
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #c7d2fe;
    border-left: 6px solid #7c3aed;
    box-shadow: 0px 6px 15px rgba(
        79,
        70,
        229,
        0.15
    );
    transition: transform 0.2s ease;
}


/* METRIC HOVER EFFECT */

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
}


/* METRIC LABEL */

div[data-testid="stMetricLabel"] {
    font-weight: 600;
    color: #4338ca;
}


/* METRIC VALUE */

div[data-testid="stMetricValue"] {
    color: #1e1b4b;
    font-weight: 800;
}

    /* DIVIDERS */

    hr {
        border: 1px solid #c7d2fe;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="ShopAI",

    page_icon="🛍️",

    layout="wide"

)


# ==========================================
# SESSION STATE
# ==========================================

if "wishlist" not in st.session_state:

    st.session_state.wishlist = []


if "cart" not in st.session_state:

    st.session_state.cart = []


if "reviews" not in st.session_state:

    st.session_state.reviews = {}


if "request_history" not in st.session_state:

    st.session_state.request_history = []


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛍️ ShopAI")

st.sidebar.write(
    "AI-Powered Shopping & Bundle Agent"
)

st.sidebar.divider()

st.sidebar.subheader("📌 Features")

st.sidebar.markdown("[🔍 Search Products](#search-products)")

st.sidebar.markdown("[🤖 Ask ShopAI](#ask-shopai)")

st.sidebar.markdown("[⚖️ Compare Products](#compare-products)")

st.sidebar.markdown("[❤️ Wishlist](#my-wishlist)")

st.sidebar.markdown("[🛒 Shopping Cart](#my-shopping-cart)")

st.sidebar.markdown("[⭐ Product Reviews](#product-reviews)")

st.sidebar.markdown("[📦 Smart Bundles](#smart-product-bundles)")

st.sidebar.markdown("[📊 Merchant Insights](#merchant-ai-insights)")
st.sidebar.divider()

st.sidebar.info(
    "💡 Describe your needs and budget "
    "in Ask ShopAI for smart recommendations."
)


# ==========================================
# MAIN TITLE
# ==========================================

st.title("🛍️ ShopAI")

st.subheader(
    "AI-Powered Shopping & Bundle Agent"
)

st.write(
    "Tell ShopAI what you need, your budget, "
    "and your preferences. Discover products, "
    "compare options, save favourites, and "
    "build smart bundles."
)


# ==========================================
# QUICK STATS
# ==========================================

total_products = len(products)


available_products_count = len(

    [

        product

        for product in products

        if product["stock"]

    ]

)


wishlist_count = len(
    st.session_state.wishlist
)


cart_count = len(
    st.session_state.cart
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🛍️ Products",
        total_products
    )


with col2:

    st.metric(
        "✅ Available",
        available_products_count
    )


with col3:

    st.metric(
        "❤️ Wishlist",
        wishlist_count
    )


with col4:

    st.metric(
        "🛒 Cart",
        cart_count
    )


st.divider()


# ==========================================
# CART & WISHLIST SUMMARY
# ==========================================

summary_col1, summary_col2 = st.columns(2)


with summary_col1:

    st.info(

        f"❤️ You have {wishlist_count} "
        f"product(s) in your wishlist."

    )


with summary_col2:

    cart_total = sum(

        product["price"]

        for product in products

        if product["id"]
        in st.session_state.cart

    )


    st.info(

        f"🛒 Your cart contains {cart_count} "
        f"item(s) worth ₹{cart_total}."

    )


st.divider()

# ==========================================
# EXPLORE CATEGORIES
# ==========================================

st.header("🗂️ Explore Categories")

categories = sorted(
    list(
        {
            product["category"]
            for product in products
        }
    )
)

selected_category = st.selectbox(
    "Choose a category",
    ["All Categories"] + categories,
    key="category_filter"
)


# ==========================================
# PRODUCT SEARCH
# ==========================================

st.header("🔍 Search Products")

search_query = st.text_input(
    "Search by product name, category, tag, or description",
    placeholder="Example: headphones, college, gift, laptop...",
    key="product_search"
)


# ==========================================
# PRICE FILTER
# ==========================================

st.header("💰 Filter by Price")

max_product_price = max(
    product["price"]
    for product in products
)

selected_price = st.slider(
    "Maximum Budget (₹)",
    min_value=0,
    max_value=max_product_price,
    value=max_product_price,
    step=100,
    key="price_filter"
)


# ==========================================
# SORT PRODUCTS
# ==========================================

st.header("↕️ Sort Products")

sort_option = st.selectbox(
    "Sort products by",
    [
        "Default",
        "Price: Low to High",
        "Price: High to Low",
        "Rating: High to Low",
        "Name: A to Z"
    ],
    key="sort_products"
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_products = products.copy()


# CATEGORY FILTER

if selected_category != "All Categories":

    filtered_products = [

        product

        for product in filtered_products

        if product["category"] == selected_category

    ]


# SEARCH FILTER

if search_query.strip():

    query = search_query.lower().strip()

    filtered_products = [

        product

        for product in filtered_products

        if (
            query in product["name"].lower()

            or query in product["category"].lower()

            or query in product["description"].lower()

            or any(
                query in tag.lower()
                for tag in product["tags"]
            )
        )

    ]


# PRICE FILTER

filtered_products = [

    product

    for product in filtered_products

    if product["price"] <= selected_price

]


# ==========================================
# APPLY SORTING
# ==========================================

if sort_option == "Price: Low to High":

    filtered_products = sorted(
        filtered_products,
        key=lambda product: product["price"]
    )


elif sort_option == "Price: High to Low":

    filtered_products = sorted(
        filtered_products,
        key=lambda product: product["price"],
        reverse=True
    )


elif sort_option == "Rating: High to Low":

    filtered_products = sorted(
        filtered_products,
        key=lambda product: product["rating"],
        reverse=True
    )


elif sort_option == "Name: A to Z":

    filtered_products = sorted(
        filtered_products,
        key=lambda product: product["name"].lower()
    )


# ==========================================
# FILTER RESULT SUMMARY
# ==========================================

st.success(
    f"🔎 Found {len(filtered_products)} matching product(s)"
)

st.divider()

# ==========================================
# PRODUCT CATALOG
# ==========================================

st.header("🛍️ Product Catalog")

if filtered_products:

    for product in filtered_products:

        with st.container():

            st.subheader(
                product["name"]
            )

            st.write(
                product["description"]
            )

            st.write(
                f"**Category:** {product['category']} "
                f"| ⭐ Rating: {product['rating']}"
            )

            st.write(
                f"**Tags:** {', '.join(product['tags'])}"
            )


            # PRODUCT INFORMATION

            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.write(
                    f"### ₹{product['price']}"
                )

            with info_col2:

                if product["stock"]:

                    st.success("✅ In Stock")

                else:

                    st.error("❌ Out of Stock")


            # WISHLIST AND CART BUTTONS

            button_col1, button_col2 = st.columns(2)


            # ❤️ WISHLIST

            with button_col1:

                if product["id"] in st.session_state.wishlist:

                    if st.button(
                        "💔 Remove from Wishlist",
                        key=f"remove_wishlist_{product['id']}"
                    ):

                        st.session_state.wishlist.remove(
                            product["id"]
                        )

                        st.rerun()

                else:

                    if st.button(
                        "❤️ Add to Wishlist",
                        key=f"add_wishlist_{product['id']}"
                    ):

                        st.session_state.wishlist.append(
                            product["id"]
                        )

                        st.rerun()


            # 🛒 CART

            with button_col2:

                if product["stock"]:

                    if product["id"] in st.session_state.cart:

                        if st.button(
                            "🗑️ Remove from Cart",
                            key=f"remove_cart_{product['id']}"
                        ):

                            st.session_state.cart.remove(
                                product["id"]
                            )

                            st.rerun()

                    else:

                        if st.button(
                            "🛒 Add to Cart",
                            key=f"add_cart_{product['id']}"
                        ):

                            st.session_state.cart.append(
                                product["id"]
                            )

                            st.success(
                                f"{product['name']} added to cart!"
                            )

                            st.rerun()

                else:

                    st.warning(
                        "Currently unavailable"
                    )


            st.divider()


else:

    st.warning(
        "No products found. "
        "Try changing your search or filters."
    )


st.divider()
# ==========================================
# MY WISHLIST
# ==========================================

st.header("❤️ My Wishlist")


wishlist_products = [

    product

    for product in products

    if product["id"]
    in st.session_state.wishlist

]


if wishlist_products:

    st.write(
        f"### ❤️ Saved Products: "
        f"{len(wishlist_products)}"
    )


    for product in wishlist_products:

        wishlist_col1, wishlist_col2 = st.columns(
            [4, 1]
        )


        with wishlist_col1:

            st.write(
                f"### 🛍️ {product['name']}"
            )

            st.write(
                f"💰 Price: ₹{product['price']}"
            )

            st.write(
                f"⭐ Rating: {product['rating']}/5"
            )

            st.write(
                f"📂 Category: {product['category']}"
            )


        with wishlist_col2:

            if st.button(
                "❌ Remove",
                key=f"wishlist_section_remove_{product['id']}"
            ):

                st.session_state.wishlist.remove(
                    product["id"]
                )

                st.rerun()


        st.divider()


else:

    st.info(
        "❤️ Your wishlist is empty. "
        "Add products from the Product Catalog!"
    )


st.divider()
# ==========================================
# SHOPPING CART
# ==========================================

st.header("🛒 My Shopping Cart")


cart_products = [

    product

    for product in products

    if product["id"]
    in st.session_state.cart

]


if cart_products:

    total_price = sum(

        product["price"]

        for product in cart_products

    )


    st.write(
        f"### 🛍️ Items in Cart: "
        f"{len(cart_products)}"
    )


    # ==========================================
    # DISPLAY CART PRODUCTS
    # ==========================================

    for product in cart_products:

        cart_col1, cart_col2 = st.columns(
            [4, 1]
        )


        with cart_col1:

            st.write(
                f"### 🛍️ {product['name']}"
            )

            st.write(
                f"💰 Price: ₹{product['price']}"
            )


        with cart_col2:

            if st.button(
                "❌ Remove",
                key=f"cart_section_remove_{product['id']}"
            ):

                st.session_state.cart.remove(
                    product["id"]
                )

                st.rerun()


        st.divider()


    # ==========================================
    # TOTAL PRICE
    # ==========================================

    st.success(
        f"💰 Total Cart Price: ₹{total_price}"
    )


    # ==========================================
    # CART ACTION BUTTONS
    # ==========================================

    cart_action_col1, cart_action_col2 = st.columns(2)


    # 🗑️ CLEAR CART

    with cart_action_col1:

        if st.button(
            "🗑️ Clear Entire Cart",
            key="clear_entire_cart"
        ):

            st.session_state.cart = []

            st.rerun()


    # 🧾 CHECKOUT

    with cart_action_col2:

        if st.button(
            "🧾 Proceed to Checkout",
            key="proceed_checkout"
        ):

            st.success(
                "🎉 Order Summary Generated!"
            )

            st.write(
                "### 🧾 Your Order"
            )


            for product in cart_products:

                st.write(
                    f"🛍️ **{product['name']}** "
                    f"— ₹{product['price']}"
                )


            st.write(
                f"### 💰 Total Amount: "
                f"₹{total_price}"
            )

            st.info(
                "This is a demo checkout. "
                "No real payment is processed."
            )


else:

    st.info(
        "🛒 Your cart is empty. "
        "Add products from the Product Catalog!"
    )


st.divider()
# ==========================================
# PRODUCT COMPARISON
# ==========================================

st.header("⚖️ Compare Products")


product_names = [

    product["name"]

    for product in products

]


compare_col1, compare_col2 = st.columns(2)


with compare_col1:

    first_product_name = st.selectbox(
        "Select First Product",
        product_names,
        key="first_compare_product"
    )


with compare_col2:

    second_product_name = st.selectbox(
        "Select Second Product",
        product_names,
        index=1,
        key="second_compare_product"
    )


# ==========================================
# FIND SELECTED PRODUCTS
# ==========================================

first_product = next(

    product

    for product in products

    if product["name"] == first_product_name

)


second_product = next(

    product

    for product in products

    if product["name"] == second_product_name

)


# ==========================================
# COMPARE BUTTON
# ==========================================

if st.button(
    "⚖️ Compare Selected Products",
    key="compare_button"
):

    if first_product["id"] == second_product["id"]:

        st.warning(
            "Please select two different products."
        )

    else:

        st.subheader(
            "📊 Product Comparison"
        )


        comparison_col1, comparison_col2 = st.columns(2)


        with comparison_col1:

            st.write(
                f"## 🛍️ {first_product['name']}"
            )

            st.write(
                f"💰 **Price:** "
                f"₹{first_product['price']}"
            )

            st.write(
                f"⭐ **Rating:** "
                f"{first_product['rating']}/5"
            )

            st.write(
                f"📂 **Category:** "
                f"{first_product['category']}"
            )

            st.write(
                f"🏷️ **Tags:** "
                f"{', '.join(first_product['tags'])}"
            )

            if first_product["stock"]:

                st.success("✅ In Stock")

            else:

                st.error("❌ Out of Stock")


        with comparison_col2:

            st.write(
                f"## 🛍️ {second_product['name']}"
            )

            st.write(
                f"💰 **Price:** "
                f"₹{second_product['price']}"
            )

            st.write(
                f"⭐ **Rating:** "
                f"{second_product['rating']}/5"
            )

            st.write(
                f"📂 **Category:** "
                f"{second_product['category']}"
            )

            st.write(
                f"🏷️ **Tags:** "
                f"{', '.join(second_product['tags'])}"
            )

            if second_product["stock"]:

                st.success("✅ In Stock")

            else:

                st.error("❌ Out of Stock")


        # ==========================================
        # QUICK COMPARISON RESULT
        # ==========================================

        st.divider()

        if first_product["price"] < second_product["price"]:

            st.info(
                f"💰 {first_product['name']} "
                f"is cheaper."
            )

        elif second_product["price"] < first_product["price"]:

            st.info(
                f"💰 {second_product['name']} "
                f"is cheaper."
            )

        else:

            st.info(
                "💰 Both products have the same price."
            )


        if first_product["rating"] > second_product["rating"]:

            st.success(
                f"⭐ {first_product['name']} "
                f"has a higher rating."
            )

        elif second_product["rating"] > first_product["rating"]:

            st.success(
                f"⭐ {second_product['name']} "
                f"has a higher rating."
            )

        else:

            st.success(
                "⭐ Both products have the same rating."
            )


st.divider()
# ==========================================
# PRODUCT REVIEWS
# ==========================================

st.header("⭐ Product Reviews")


# SELECT PRODUCT

review_product_name = st.selectbox(
    "Select a product to review",
    [product["name"] for product in products],
    key="review_product_select"
)


selected_review_product = next(
    product
    for product in products
    if product["name"] == review_product_name
)


# ==========================================
# REVIEW INPUT
# ==========================================

user_rating = st.slider(
    "Your Rating",
    min_value=1,
    max_value=5,
    value=5,
    key="user_rating"
)


user_review = st.text_area(
    "Write your review",
    placeholder=(
        "Tell us what you think about "
        "this product..."
    ),
    key="user_review"
)


# ==========================================
# SUBMIT REVIEW
# ==========================================

if st.button(
    "⭐ Submit Review",
    key="submit_review"
):

    product_id = selected_review_product["id"]


    if product_id not in st.session_state.reviews:

        st.session_state.reviews[product_id] = []


    if user_review.strip():

        st.session_state.reviews[product_id].append(

            {
                "rating": user_rating,
                "review": user_review.strip()
            }

        )

        st.success(
            "🎉 Thank you! Your review was submitted."
        )

        st.rerun()


    else:

        st.warning(
            "⚠️ Please write a review "
            "before submitting."
        )


# ==========================================
# DISPLAY REVIEWS
# ==========================================

st.divider()

st.subheader("📝 Customer Reviews")


product_id = selected_review_product["id"]


if (
    product_id in st.session_state.reviews
    and st.session_state.reviews[product_id]
):

    reviews = st.session_state.reviews[product_id]


    # AVERAGE RATING

    average_rating = sum(

        review["rating"]

        for review in reviews

    ) / len(reviews)


    st.success(
        f"⭐ Average User Rating: "
        f"{average_rating:.1f}/5"
    )


    st.write(
        f"📝 Total Reviews: {len(reviews)}"
    )


    # SHOW EACH REVIEW

    for index, review in enumerate(
        reviews,
        start=1
    ):

        with st.container():

            st.write(
                f"### Review {index}"
            )

            st.write(
                f"⭐ Rating: "
                f"{review['rating']}/5"
            )

            st.write(
                f"💬 {review['review']}"
            )

            st.divider()


else:

    st.info(
        "No reviews yet for this product. "
        "Be the first to write one! ⭐"
    )


st.divider()

# ==========================================
# ASK SHOPAI - AI RECOMMENDATION SYSTEM
# ==========================================

st.header("🤖 Ask ShopAI")

st.write(
    "Describe what you are looking for. "
    "You can include your purpose, interests, "
    "budget, or preferences."
)


user_request = st.text_area(
    "What are you looking for?",
    placeholder=(
        "Example: I need a gift for a friend "
        "under 1500 for their birthday"
    ),
    key="shopai_request"
)


user_budget = st.number_input(
    "Your Budget (₹)",
    min_value=0,
    value=2000,
    step=100,
    key="shopai_budget"
)


# ==========================================
# RECOMMENDATION BUTTON
# ==========================================

if st.button(
    "🤖 Get ShopAI Recommendations",
    key="get_shopai_recommendations"
):

    if user_request.strip():

        request = user_request.lower().strip()


        # ==========================================
        # SAVE REQUEST HISTORY
        # ==========================================

        st.session_state.request_history.append(
            {
                "request": user_request.strip(),
                "budget": user_budget
            }
        )


        # ==========================================
        # FIND KEYWORDS
        # ==========================================

        request_words = request.split()


        # ==========================================
        # MATCH PRODUCTS
        # ==========================================

        recommended_products = []


        for product in products:

            if not product["stock"]:
                continue


            # PRODUCT SEARCH TEXT

            product_text = (
                product["name"].lower()
                + " "
                + product["category"].lower()
                + " "
                + product["description"].lower()
                + " "
                + " ".join(product["tags"]).lower()
            )


            # SCORE PRODUCT

            score = 0


            for word in request_words:

                if word in product_text:

                    score += 1


            # BUDGET BONUS

            if product["price"] <= user_budget:

                score += 1


            # ADD MATCHING PRODUCT

            if score > 0:

                recommended_products.append(
                    {
                        "product": product,
                        "score": score
                    }
                )


        # ==========================================
        # SORT RECOMMENDATIONS
        # ==========================================

        recommended_products = sorted(

            recommended_products,

            key=lambda item: (
                item["score"],
                item["product"]["rating"]
            ),

            reverse=True

        )


        # ==========================================
        # DISPLAY RESULTS
        # ==========================================

        st.divider()

        st.subheader(
            "✨ ShopAI Recommendations"
        )


        # PRODUCTS WITHIN BUDGET

        within_budget = [

            item

            for item in recommended_products

            if item["product"]["price"]
            <= user_budget

        ]


        if within_budget:

            st.success(
                f"🎯 Found {len(within_budget)} "
                f"recommendation(s) within "
                f"your ₹{user_budget} budget!"
            )


            for index, item in enumerate(
                within_budget[:5],
                start=1
            ):

                product = item["product"]


                st.write(
                    f"### {index}. 🛍️ "
                    f"{product['name']}"
                )

                st.write(
                    product["description"]
                )

                st.write(
                    f"💰 Price: ₹{product['price']} "
                    f"| ⭐ Rating: {product['rating']}/5"
                )

                st.write(
                    f"🏷️ Tags: "
                    f"{', '.join(product['tags'])}"
                )


                # EXPLANATION

                st.info(
                    f"🧠 Why ShopAI recommends this: "
                    f"It matches your request and "
                    f"fits within your ₹{user_budget} budget."
                )

                st.divider()


        else:

            st.warning(
                "No strong matches were found "
                "within your budget."
            )


            # ==========================================
            # SMART ALTERNATIVES
            # ==========================================

            affordable_products = [

                product

                for product in products

                if product["stock"]
                and product["price"] <= user_budget

            ]


            affordable_products = sorted(

                affordable_products,

                key=lambda product: product["rating"],

                reverse=True

            )


            if affordable_products:

                st.subheader(
                    "🔄 Smart Alternatives"
                )

                st.write(
                    "Here are some highly rated "
                    "products within your budget:"
                )


                for product in affordable_products[:5]:

                    st.write(
                        f"🛍️ **{product['name']}** "
                        f"— ₹{product['price']} "
                        f"| ⭐ {product['rating']}"
                    )


    else:

        st.warning(
            "⚠️ Please describe what you are "
            "looking for first."
        )


st.divider()
# ==========================================
# SMART PRODUCT BUNDLES
# ==========================================

st.header("📦 Smart Product Bundles")

st.write(
    "ShopAI can combine products into useful "
    "2-product and 3-product bundles."
)


# AVAILABLE PRODUCTS

available_products = [

    product

    for product in products

    if product["stock"]

]


# ==========================================
# 2-PRODUCT BUNDLES
# ==========================================

st.subheader("📦 2-Product Bundles")


bundle_2_budget = st.number_input(
    "Budget for 2-product bundle (₹)",
    min_value=0,
    value=2000,
    step=100,
    key="bundle_2_budget"
)


two_product_bundles = []


for i in range(len(available_products)):

    for j in range(
        i + 1,
        len(available_products)
    ):

        product1 = available_products[i]

        product2 = available_products[j]


        bundle_price = (

            product1["price"]
            + product2["price"]

        )


        if bundle_price <= bundle_2_budget:

            two_product_bundles.append(

                {
                    "products": [
                        product1,
                        product2
                    ],

                    "price": bundle_price,

                    "rating": (
                        product1["rating"]
                        + product2["rating"]
                    ) / 2

                }

            )


# SORT BY RATING

two_product_bundles = sorted(

    two_product_bundles,

    key=lambda bundle: (
        bundle["rating"],
        -bundle["price"]
    ),

    reverse=True

)


if two_product_bundles:

    for index, bundle in enumerate(
        two_product_bundles[:3],
        start=1
    ):

        st.write(
            f"### 🎁 Bundle {index}"
        )


        for product in bundle["products"]:

            st.write(
                f"🛍️ **{product['name']}** "
                f"— ₹{product['price']}"
            )


        st.success(
            f"💰 Bundle Price: "
            f"₹{bundle['price']}"
        )


        st.write(
            f"⭐ Average Rating: "
            f"{bundle['rating']:.1f}/5"
        )


        st.divider()


else:

    st.info(
        "No 2-product bundles found "
        "within this budget."
    )


# ==========================================
# 3-PRODUCT BUNDLES
# ==========================================

st.subheader("📦 3-Product Bundles")


bundle_3_budget = st.number_input(
    "Budget for 3-product bundle (₹)",
    min_value=0,
    value=3000,
    step=100,
    key="bundle_3_budget"
)


three_product_bundles = []


for i in range(len(available_products)):

    for j in range(
        i + 1,
        len(available_products)
    ):

        for k in range(
            j + 1,
            len(available_products)
        ):

            product1 = available_products[i]

            product2 = available_products[j]

            product3 = available_products[k]


            bundle_price = (

                product1["price"]
                + product2["price"]
                + product3["price"]

            )


            if bundle_price <= bundle_3_budget:

                three_product_bundles.append(

                    {
                        "products": [
                            product1,
                            product2,
                            product3
                        ],

                        "price": bundle_price,

                        "rating": (

                            product1["rating"]
                            + product2["rating"]
                            + product3["rating"]

                        ) / 3

                    }

                )


# SORT 3-PRODUCT BUNDLES

three_product_bundles = sorted(

    three_product_bundles,

    key=lambda bundle: (
        bundle["rating"],
        -bundle["price"]
    ),

    reverse=True

)


if three_product_bundles:

    for index, bundle in enumerate(
        three_product_bundles[:3],
        start=1
    ):

        st.write(
            f"### 🎁 Bundle {index}"
        )


        for product in bundle["products"]:

            st.write(
                f"🛍️ **{product['name']}** "
                f"— ₹{product['price']}"
            )


        st.success(
            f"💰 Bundle Price: "
            f"₹{bundle['price']}"
        )


        st.write(
            f"⭐ Average Rating: "
            f"{bundle['rating']:.1f}/5"
        )


        st.divider()


else:

    st.info(
        "No 3-product bundles found "
        "within this budget."
    )


# ==========================================
# BUNDLE COMPATIBILITY CHECKER
# ==========================================

st.header("🧩 Bundle Compatibility Checker")

st.write(
    "Select products and let ShopAI check "
    "how well their purposes and tags match."
)


compatibility_product_names = [

    product["name"]

    for product in available_products

]


selected_bundle_products = st.multiselect(
    "Select 2 or more products",
    compatibility_product_names,
    key="compatibility_products"
)


if st.button(
    "🧩 Check Compatibility",
    key="check_compatibility"
):

    if len(selected_bundle_products) < 2:

        st.warning(
            "Please select at least "
            "2 products."
        )


    else:

        selected_products = [

            product

            for product in available_products

            if product["name"]
            in selected_bundle_products

        ]


        all_tags = []


        for product in selected_products:

            all_tags.extend(
                product["tags"]
            )


        common_tags = set(

            tag

            for tag in all_tags

            if all_tags.count(tag) > 1

        )


        if common_tags:

            st.success(
                "🤝 Good Compatibility!"
            )

            st.write(
                f"🔗 Common purposes: "
                f"{', '.join(common_tags)}"
            )


        else:

            st.info(
                "⚖️ Mixed Bundle: These products "
                "serve different purposes, but "
                "can still be useful together."
            )


        total_bundle_price = sum(

            product["price"]

            for product in selected_products

        )


        st.write(
            f"💰 Combined Price: "
            f"₹{total_bundle_price}"
        )


# ==========================================
# REQUEST HISTORY
# ==========================================

st.header("📜 Your ShopAI Request History")


if st.session_state.request_history:

    for index, item in enumerate(
        reversed(
            st.session_state.request_history
        ),
        start=1
    ):

        st.write(
            f"### Request {index}"
        )

        st.write(
            f"💬 **Request:** "
            f"{item['request']}"
        )

        st.write(
            f"💰 **Budget:** "
            f"₹{item['budget']}"
        )

        st.divider()


else:

    st.info(
        "No ShopAI requests yet. "
        "Use Ask ShopAI to get recommendations!"
    )


st.divider()
# ==========================================
# MERCHANT INSIGHTS
# ==========================================

st.header("📊 Merchant AI Insights")

st.write(
    "These insights help understand product "
    "performance and customer interest."
)


# ==========================================
# PRODUCT STATISTICS
# ==========================================

total_products = len(products)

in_stock_products = len(

    [
        product

        for product in products

        if product["stock"]
    ]

)

out_of_stock_products = (
    total_products - in_stock_products
)


average_product_price = sum(

    product["price"]

    for product in products

) / total_products


average_product_rating = sum(

    product["rating"]

    for product in products

) / total_products


# ==========================================
# DISPLAY METRICS
# ==========================================

insight_col1, insight_col2, insight_col3, insight_col4 = (
    st.columns(4)
)


with insight_col1:

    st.metric(
        "🛍️ Total Products",
        total_products
    )


with insight_col2:

    st.metric(
        "✅ In Stock",
        in_stock_products
    )


with insight_col3:

    st.metric(
        "💰 Average Price",
        f"₹{average_product_price:.0f}"
    )


with insight_col4:

    st.metric(
        "⭐ Average Rating",
        f"{average_product_rating:.1f}/5"
    )


# ==========================================
# CATEGORY INSIGHTS
# ==========================================

st.subheader("📂 Category Insights")


category_counts = {}


for product in products:

    category = product["category"]

    if category not in category_counts:

        category_counts[category] = 0

    category_counts[category] += 1


for category, count in category_counts.items():

    st.write(
        f"📦 **{category}:** "
        f"{count} product(s)"
    )


# ==========================================
# CUSTOMER INTEREST
# ==========================================

st.subheader("❤️ Customer Interest")


wishlist_count = len(
    st.session_state.wishlist
)

cart_count = len(
    st.session_state.cart
)

review_count = sum(

    len(review_list)

    for review_list
    in st.session_state.reviews.values()

)


interest_col1, interest_col2, interest_col3 = (
    st.columns(3)
)


with interest_col1:

    st.metric(
        "❤️ Wishlist Items",
        wishlist_count
    )


with interest_col2:

    st.metric(
        "🛒 Cart Items",
        cart_count
    )


with interest_col3:

    st.metric(
        "⭐ Reviews Submitted",
        review_count
    )


# ==========================================
# POPULAR PRODUCTS
# ==========================================

st.subheader("🏆 Highest Rated Products")


highest_rated_products = sorted(

    products,

    key=lambda product: product["rating"],

    reverse=True

)


for index, product in enumerate(
    highest_rated_products[:5],
    start=1
):

    st.write(
        f"{index}. 🏆 **{product['name']}** "
        f"— ⭐ {product['rating']}/5 "
        f"| ₹{product['price']}"
    )


# ==========================================
# REQUEST INSIGHTS
# ==========================================

st.subheader("🤖 ShopAI Usage Insights")


total_requests = len(
    st.session_state.request_history
)


if total_requests > 0:

    average_request_budget = sum(

        item["budget"]

        for item
        in st.session_state.request_history

    ) / total_requests


    st.success(
        f"📈 Total ShopAI Requests: "
        f"{total_requests}"
    )


    st.write(
        f"💰 Average Customer Budget: "
        f"₹{average_request_budget:.0f}"
    )


else:

    st.info(
        "No ShopAI requests have been made yet."
    )


st.divider()


# ==========================================
# WHAT SHOPAI WILL DO
# ==========================================

st.header("✨ What ShopAI Will Do")

st.write("🤖 Intent-Based Shopping")

st.write("📦 Dynamic 2-Product Bundles")

st.write("📦 Dynamic 3-Product Bundles")

st.write("🤝 AI Constraint Negotiation")

st.write("🎯 Goal Coverage")

st.write("⚖️ Bundle Trade-Off Comparison")

st.write("🧠 Explainable Recommendations")

st.write("🔄 Smart Alternative Finder")

st.write("🧩 Bundle Compatibility Checker")

st.write("📊 Merchant AI Insights")


st.divider()


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div style="text-align: center;">
        <h3>🛍️ ShopAI</h3>
        <p>
            AI-Powered Shopping & Bundle Agent
        </p>
        <p>
            Built with Python and Streamlit 🚀
        </p>
    </div>
    """,
    unsafe_allow_html=True
)