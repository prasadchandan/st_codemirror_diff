import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_codemirror",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "streamlit_codemirror", path=build_dir
    )


def streamlit_codemirror(name, left, right, opts, key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    component_value = _component_func(name=name, left=left, right=right, opts=opts, key=key, default=0)
    return component_value

def streamlit_codemirror_options(loc):
    ln = loc.checkbox("Line Numbers", value=True)
    collapse = loc.checkbox("Collapse Identical", value=True)
    cn = loc.selectbox("Align Diffs.", ('Default', 'Align'))
    theme = loc.selectbox('Theme', ('Eclipse', 'Neat', 'MDN-Like', 'Idea'))
    language = loc.selectbox('Syntax Highlighting', ('C Like', 'Python', 'Shell'))
    opts = {
        "line_numbers": ln,
        "connect": None if cn == 'Default' else cn.lower(),
        "theme": theme.lower(),
        "collapse": collapse,
        "language": language.replace(" ", "").lower(),
    }
    return opts


if not _RELEASE:
    import streamlit as st
    st.set_page_config(
        page_title="CodeMirror - DiffMergeView Component",
        layout="wide"
    )
    st.subheader("Diff Merge View")

    left_content = """#include <iostream>

//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code

int main() {
  // Some comment
  return 0;
}"""

    right_content = """#include <iostream>
#include <cstdio>
Test

//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code
//This is a common segment of code

int main() {
  int a, b;
  std::cout << "A: " << a << " B: " << b << std::endl;

  return 0;
}"""
    opts = streamlit_codemirror_options(st.sidebar)

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    with st.beta_expander("Show diff"):
        num_clicks = streamlit_codemirror("World", left_content, right_content, opts)
