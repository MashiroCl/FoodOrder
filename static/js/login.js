function mdclick() {
        $.ajax({
            url:"http://127.0.0.1:8000/test1",            //!!!!!!!!!!!!!!
            data:{},
            type: "POST",
            dataType:'json',
           success: function (result) {
                    console.log('成功');
                },
                fail: function (result) {
                    console.log('失败');
                }
            }).done(function (data) {    //回调函数获取的data就是view返回的json数据
                alert("jifdosjfoiasdf");
                var jsonData = JSON.parse(data);
                alert(data);
                $("#name").text(jsonData.data);
        }
        );

}