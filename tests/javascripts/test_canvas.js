// alert("Hello from JavaScript!");


(function () {
    // 获取 Canvas 元素
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");

    // 绘制矩形
    ctx.fillStyle = "#FF0000"; // 设置填充颜色
    ctx.fillRect(20, 20, 150, 100); // 绘制矩形

    // 绘制圆形
    ctx.beginPath(); // 开始路径
    ctx.arc(240, 70, 50, 0, Math.PI * 2); // 绘制圆
    ctx.fillStyle = "blue"; // 设置填充颜色
    ctx.fill(); // 填充圆形

    // 绘制文本
    ctx.font = "30px Arial";
    ctx.fillStyle = "green";
    ctx.fillText("Hello Canvas!", 10, 250);
}());