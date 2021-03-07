import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_codemirror_diff",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "st_codemirror_diff", path=build_dir
    )


def st_codemirror_diff(left, right, opts, key=None):
    """Create a new instance of "st_codemirror_diff".

    Parameters
    ----------
    left: str
        Content to display in the left panel of the diff view.
    right: str
        Content to display in the right panel of the diff view.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    None

    """
    component_value = _component_func(left=left, right=right, opts=opts, key=key, default=0)
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
        page_title="Streamlit CodeMirror diff view component",
        layout="wide"
    )
    st.subheader("CodeMirror diff-view Component")

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
  std::cout << "A: " << a << " B: " 
            << b << std::endl;

  return 0;
}"""
    opts = streamlit_codemirror_options(st.sidebar)
    num_clicks = st_codemirror_diff(left_content, right_content, opts)
