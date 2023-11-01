const sidebarDropBtnList = document.querySelectorAll(".drop-btn");

for (const sidebarDropBtnElement of sidebarDropBtnList) {
    const dropDownMenu = sidebarDropBtnElement.closest('li').querySelector('.drop-down-menu')
    const btn = sidebarDropBtnElement.parentElement;
    const dropDownMenuChildrenCount = dropDownMenu.childElementCount;

    sidebarDropBtnElement.onclick = () => {
        sidebarDropBtnElement.classList.toggle("clicked");
        if (dropDownMenu.style.maxHeight) {
            dropDownMenu.style.maxHeight = null;
            btn.style.backgroundColor = null;
        } else {
            dropDownMenu.style.maxHeight = (dropDownMenuChildrenCount * 3.7) + "rem";
            btn.style.backgroundColor = getComputedStyle(btn).getPropertyValue('--gray-lighter');
        }
    }
}
