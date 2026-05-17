import streamlit as st
from streamlit_extras.steps import steps



def example_emoji_icons() -> None:
    s = steps(
        ["Idea", "Build", "Test", "Ship"],
        icons=["💡", "🔨", "🧪", "🚀"],
        key="demo_emoji",
    )

    with s[0]:
        st.write("Brainstorm your idea.")
        if st.button("Next", key="em_next_0"):
            s.next()

    with s[1]:
        st.write("Build the prototype.")
        if st.button("Next", key="em_next_1"):
            s.next()

    with s[2]:
        st.write("Run your tests.")
        if st.button("Next", key="em_next_2"):
            s.next()

    with s[3]:
        st.success("Shipped!")
        if st.button("Start over", key="em_reset"):
            s.reset()


def example_material_icons() -> None:
    _labels = ["Cart", "Shipping", "Payment", "Done"]
    h_steps = steps(
        _labels,
        horizontal=True,
        icons=[
            ":material/shopping_cart:",
            ":material/local_shipping:",
            ":material/payment:",
            ":material/check_circle:",
        ],
        key="demo_hd",
    )

    with h_steps[0]:
        st.write("Review your cart items.")
        if st.button("Next", key="hd_next_0"):
            h_steps.next()

    with h_steps[1]:
        st.write("Enter shipping details.")
        if st.button("Next", key="hd_next_1"):
            h_steps.next()

    with h_steps[2]:
        st.write("Complete payment.")
        if st.button("Next", key="hd_next_2"):
            h_steps.next()

    with h_steps[3]:
        st.balloons()
        st.success("Order placed!")
        if st.button("New order", key="hd_reset"):
            h_steps.reset()

def example_vertical_dots() -> None:
    s = steps(
        ["Connect", "Configure", "Deploy", "Monitor"],
        key="demo_vd",
    )

    with s[0]:
        st.write("Connect to your data source.")
        if st.button("Next", key="vd_next_0"):
            s.next()

    with s[1]:
        st.write("Set up your pipeline configuration.")
        if st.button("Next", key="vd_next_1"):
            s.next()

    with s[2]:
        st.write("Deploy to production.")
        if st.button("Next", key="vd_next_2"):
            s.next()

    with s[3]:
        st.write("Monitor your deployment.")
        if st.button("Reset", key="vd_reset"):
            s.reset()


def example_jump_to_step() -> None:
    s = steps(
        ["Intro", "Details", "Review", "Submit"],
        icons=range(1, 5),
        key="demo_jump",
    )

    with s[0]:
        st.write("Welcome! Jump to any step:")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Go to Details", key="j_1"):
                s.set(1)
        with c2:
            if st.button("Go to Review", key="j_2"):
                s.set(2)
        with c3:
            if st.button("Go to Submit", key="j_3"):
                s.set(3)

    with s[1]:
        st.write("Fill in your details.")
        if st.button("Back", key="j_back_1"):
            s.previous()

    with s[2]:
        st.write("Review everything.")
        if st.button("Back", key="j_back_2"):
            s.previous()

    with s[3]:
        st.write("Ready to submit!")
        if st.button("Reset", key="j_reset"):
            s.reset()


st.title("📄 Documents")
st.markdown(
    """
    This page is a placeholder for document-related features. You can use it to upload, view, and manage your documents in the future.
    """
)

st.subheader("Examples of Stepper Component")
st.markdown("Here are some examples of how to use the `steps` component from `streamlit_extras` to create interactive step-by-step workflows in your Streamlit app.")           
example_emoji_icons()
example_material_icons()
example_vertical_dots()

example_jump_to_step()