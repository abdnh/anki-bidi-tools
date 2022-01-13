// https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements
const BLOCK_ELEMENTS = [
    "ADDRESS",
    "ARTICLE",
    "ASIDE",
    "BLOCKQUOTE",
    "DETAILS",
    "DIALOG",
    "DD",
    "DIV",
    "DL",
    "DT",
    "FIELDSET",
    "FIGCAPTION",
    "FIGURE",
    "FOOTER",
    "FORM",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "HEADER",
    "HGROUP",
    "HR",
    "LI",
    "MAIN",
    "NAV",
    "OL",
    "P",
    "PRE",
    "SECTION",
    "TABLE",
    "UL",
];

function BidiToolsElementIsBlock(element) {
    return BLOCK_ELEMENTS.includes(element.tagName);
}

function BidiToolsNodeIsElement(node) {
    return node.nodeType === Node.ELEMENT_NODE;
}

function BidiToolsSetInlineDir(dir) {
    const currentField = document.activeElement.shadowRoot;
    let selection = currentField.getSelection();
    let anchor = selection.anchorNode;
    let element = anchor;
    // Find deepest inline element that contains the anchor and change its direction
    if (BidiToolsNodeIsElement(element) && !BidiToolsElementIsBlock(element) && element.tagName !== "ANKI-EDITABLE") {
        element.dir = dir;
    }
    else {
        // Add a new element otherwise
        wrap(`<bdi dir="${dir}">`, "</bdi>");
    }
}

function BidiToolsSetBlockDir(dir) {
    const currentField = document.activeElement.shadowRoot;
    let selection = currentField.getSelection();
    let anchor = selection.anchorNode;
    let element = anchor;
    // Find deepest block element that contains the anchor
    while (!BidiToolsElementIsBlock(element) && element.parentElement.tagName !== "ANKI-EDITABLE") {
        element = element.parentElement;
    }
    // If the outermost node in the field is not a block element, add a div
    if (!BidiToolsElementIsBlock(element)) {
        document.execCommand("formatBlock", false, "DIV");
        selection = currentField.getSelection();
        anchor = selection.anchorNode;
        element = BidiToolsNodeIsElement(anchor) ? anchor : anchor.parentElement;
    }
    element.dir = dir;
}
