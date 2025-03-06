const search = document.getElementById('search');
const searchValue = search.value.toLowerCase();

// console.log(searchValue);

// 获取所有卡片元素
const cards = document.querySelectorAll('.nicegui-card');

// 遍历每个卡片
cards.forEach(card => {
    const text = card.textContent.toLowerCase();

    // if (text.includes(searchValue)) {
    //     console.log(text);
    // }

    // 设置可见性（通过 display 属性控制）。note: 这个太妙了，隐藏而不是删除！
    card.style.display = text.includes(searchValue)
        ? 'block'     // 显示元素
        : 'none';     // 隐藏元素
});
