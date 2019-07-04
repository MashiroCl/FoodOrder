(function ($) {
    "use strict";


    /*==================================================================
   [ Focus input ]*/
    $('.input-content').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() !== "") {
                $(this).addClass('has-val');
            } else {
                $(this).removeClass('has-val');
            }
        })
    });


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input-content');

    $('.validate-register-form').on('submit', function () {
        var check = true;

        // Validate
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) === false) {
                showValidate(input[i]);
                check = false;
            }
        }
        
        const password = $('#password-input').val();
        const verifyPassword = $('#verify-password-input').val();
        const phone = $('#phone-input').val();
        if(password !== verifyPassword) {
            alert("两次密码输入不一致，请重新输入！");
            check = false;
        }
        // if(length(phone) !== 11){
        //     alert("电话号码输入不正确，应为11位！")；
        //     check = false;
        // }
        // Register
        if (check === true) {
            const username = $('#username-input').val();

            var post_data = {
                "username": username,
                "password": password,
                "phone": phone
            };

            $.ajax({
                url: "/registerCheck",    // 待添加：注册请求url
                contentType: 'application/json',
                type: 'POST',
                data: JSON.stringify(post_data),
                success: function (result) {
                    console.log('成功');
                },
                fail: function (result) {
                    console.log('失败');
                }
            }).done(function (data) {    //回调函数获取的data就是view返回的json数据
                if (data.res === 0) {
                    alert('该用户名已被注册，请重试');
                    // $('#errmsg').show().html() //jQuery动态添加网页内容
                } else {
                    // alert('注册成功');
                    location.href = '/sign/';      //验证成功登录首页
                }
            });
        }

        return check;
    });


    $('.validate-register-form .input-content').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });

    // function validate(input) {
    //     if ($(input).attr('type') === 'text') {
    //         // 用户名：4-16位字母,数字,汉字,下划线
    //         if ($(input).val().match(/^[a-zA-Z0-9_\u4e00-\u9fa5]{4,16}$/) == null) {
                
    //             return false;
    //         }
    //     } else if ($(input).attr('type') === 'password') {
    //         // 密码：包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位
    //         if ($(input).val().match(/^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/) == null) {
    //             alert("密码格式不合法！\n密码包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位！");
    //             return false;
    //         }
    //     } else {
    //         if ($(input).val().trim() === '') {
    //             return false;
    //         }
    //     }
    // }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    /*==================================================================
    [ Get Verify Code ]*/
//     $('.get-verify-code-btn').click(function () {
//         var countdown = 0;

//         if (countdown === 0) {
//             $(this).removeAttr("disabled");
//             $(this).value = "点击获取";
//             countdown = 60;
//             var telephone = $('#telephone-input').val();
//             $.post("/register/", {
//                 phone: telephone
//             }, function (data) {
//                 /** @namespace data.messages */
//                 if (data.messages !== null && data.messages[0].code === '1000') {
//                     window.location.href = "home";
//                 } else {
//                     alert(data.messages[0].message);
//                 }
//             });
//         } else {
//             $(this).setAttribute("disabled", true);
//             $(this).value = "重新发送(" + countdown + ")";
//             $(this).border = "1px solid black";
//             countdown--;
//             if (countdown > 1) {
//                 setTimeout(function () {
//                     setTime(button)
//                 }, 1000);
//             }
//         }
//     })

})(jQuery);
