import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { ReactNode } from "react"

// @ts-ignore
import CodeMirror from 'codemirror/lib/codemirror'

import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/eclipse.css'
import 'codemirror/theme/mdn-like.css'
import 'codemirror/theme/idea.css'
import 'codemirror/theme/material.css'
import 'codemirror/theme/neat.css'

import 'codemirror/mode/clike/clike'
import 'codemirror/mode/python/python'
import 'codemirror/mode/shell/shell'

import "codemirror/addon/fold/foldgutter.css"
import "codemirror/addon/fold/foldgutter.js"
import "codemirror/addon/fold/foldcode"
import "codemirror/addon/fold/brace-fold"
import "codemirror/addon/fold/comment-fold"

import 'codemirror/addon/merge/merge.css'
import 'codemirror/addon/merge/merge.js';
import 'codemirror/addon/merge/merge'
import "codemirror/addon/selection/active-line"

interface State {
  numClicks: number
  leftContent: string
  rightContent: string
  opts: object
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class DiffMergeView extends StreamlitComponentBase<State> {
  public state = { 
    numClicks: 0,
    leftContent: 'ABC',
    rightContent: 'BCD',
    opts: {}
  }

  public diffmergeref: any | null = null;
  setDiffViewRef = (element): void  => {
    this.diffmergeref = element; 
  }

  renderDiffMergeView(props) {
    CodeMirror.MergeView(this.diffmergeref, Object.assign({}, {
      theme: props.args['opts']['theme'],
      mode: props.args['opts']['language'],
      value: props.args['left'],
      orig: props.args['right'],
      lineNumbers: props.args['opts']['line_numbers'],
      highlightDifferences: 'highlight', 
      allowEditingOriginals: false,
      lint: false,
      connect: props.args['opts']['connect'], // alternative 'align'
      readOnly: true,
      revertButtons: false,
      styleActiveLine: true,
      matchBrackets: true,
      foldGutter: true,
      collapseIdentical: props.args['opts']['collapse'],
      smartIndent: true,
      spellcheck: false,
      gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
      extraKeys: {
        "Ctrl-[": "goNextDiff",
        "Ctrl-]": "goPrevDiff",
      }
    }, this.props.args['opts'] || {}));

    // FIXME This is not allowed by browsers for security reasons. 
    // Figure out an alternative way to get a full screen view.
    // this.diffmergeref.requestFullscreen();
  }

  componentDidMount(): void {
    // FIXME For some reason the diff does not render till a refresh
    // call onClicked() to force refresh
    this.renderDiffMergeView(this.props);
    this.onClicked()
  }

  // FIXME Unnecessary for now
  // componentWillReceiveProps(nextProps){
  //    this.renderDiffMergeView(nextProps);
  //}

  public render = (): ReactNode => {
    return (
      <div ref={this.setDiffViewRef} style={{height: '100%'}}></div>
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 1 }),
      () => Streamlit.setComponentValue(this.state.numClicks)
    )
  }
}

export default withStreamlitConnection(DiffMergeView)
