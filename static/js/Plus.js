//减数量
function reductionOf(obj) {
    //减前判断
    if ($(obj).next().val() == 0) {
        $(obj).next().val(1);
    }
    $(obj).next().val(parseInt($(obj).next().val()) - 1);//数值减
    $(obj).next().val($(obj).next().val());//赋值给框
};
//加数量
function add(obj) {
    //加前判断
    if ($(obj).prev().val() == '') {
        $(obj).prev().val(1);
    }
    $(obj).prev().val(parseInt($(obj).prev().val()) + 1);//数值加
    $(obj).prev().val($(obj).prev().val());//赋值给框
};
//校验数字格式（只能输入正整数）
function checkNumber(obj) {
    var reg = /^[1-9]\d*$/;
    if(!reg.test($(obj).val()) || $(obj).val()==''){
        $(obj).val(1);
    }
}

function openwindows() {
    alert("OPENWINDOW");
    Final_Settlement();
    alert("JUMP!");
    jump2();
    //window.open("http://127.0.0.1:8000/Settlement/", "newwindow", "height=800, width=800, top=200,left=400,toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no, status=no");
}
//写成一行


function Final_Settlement() {
    Dish1=$("#B11").val()
    Dish2=$("#B21").val()
    Dish3=$("#B31").val()
    var Price_in_total = $("#B11").val()*10 + $("#B21").val()*11 + $("#B31").val()*12 ;//通过id获取文本框对象;
    document.cookie=Price_in_total
    //return  "您本次点菜结果如下：\n" + "油炸大白菜 份数：" + $('#B11').val() + "\n" + "馒头蘸红糖 份数：" + $('#B21').val() + "\n" + "炖石头 份数：" + $('#B31').val() + "\n" +
     //"总计价格为： " + Price_in_total//通过文本框对象获取value值
    temp="您本次点菜结果如下：\n"
    if(Dish1!=0){
        temp=temp+"油炸大白菜 份数："+Dish1+"\n"
    }
    if(Dish2!=0){
        temp=temp+"馒头蘸红糖 份数："+Dish2+"\n"
    }
    if(Dish3!=0){
        temp=temp+"炖石头 份数："+Dish3+"\n"
    }
    alert(temp+ "总计价格为： " + Price_in_total);
}

function jump2(){
    let text = window.location.search;
    let param = text.split("?");
    let userID = decodeURIComponent(param[1].split("=")[1]);
    Dish1=$("#B11").val()
    Dish2=$("#B21").val()
    Dish3=$("#B31").val()
    var Price_in_total = $("#B11").val()*10 + $("#B21").val()*11 + $("#B31").val()*12 ;//通过id获取文本框对象;
    //document.cookie=Price_in_total
    var temp=" ";
    var orderAbbre="";
    if(Dish1!=0){
        temp=temp+"油炸大白菜 份数："+Dish1+"\n"
        orderAbbre=orderAbbre+"1_"+Dish1+",";
    }
    if(Dish2!=0){
        temp=temp+"馒头蘸红糖 份数："+Dish2+"\n"
        orderAbbre=orderAbbre+"2_"+Dish2+",";

    }
    if(Dish3!=0){
        temp=temp+"炖石头 份数："+Dish3+"\n"
        orderAbbre=orderAbbre+"3_"+Dish3+",";
    }
    let url1 = "../Settlement/?price="+Price_in_total+"?order="+temp+"?username="+userID+"?orderAbbre="+orderAbbre;//此处拼接内容
    window.open(url1);
    //window.location.href = url;
}
function Get_OrderList(){
    var res=document.cookie;
    document.getElementById("OrderList").value=res;
    return res;
}

function GetWaitingNum() {
    let text = window.location.search;
    let param = text.split("?");
    let userID = decodeURIComponent(param[3].split("=")[1]);
    let orderAbbre=decodeURIComponent(param[4].split("=")[1]);

    $.ajax({
        url:"http://127.0.0.1:8000/PayEndProcess/",
        data:{id: userID,
              dish:orderAbbre},
        type: "POST",
        datatype:"json",
        success: function (data) {
            alert("正在烹饪中，请耐心等待");
            waitingNum=JSON.parse(data.waitingNum)
            var orderNum=JSON.parse(data.orderNum)
            alert("comment = "+waitingNum);
            let url = "../waiting?waitingNum="+waitingNum+"?orderNum="+orderNum+"?orderAbbre="+orderAbbre+"?userID="+userID;
            window.location.href = url;
        },
        error:function(data){
            alert("请重新单击“支付成功”按钮重试");

        }
    });
}
