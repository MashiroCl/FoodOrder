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

    $('.validate-form').on('submit', function () {
        var check = true;


        // Validate
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) === false) {
                showValidate(input[i]);
                check = false;
            }
        }

        // Sign in
        if (check === true) {

            const username = $('#username-input').val();
            const password = $('#password-input').val();

            var post_data = {
                "username": username,
                "password": password
            };
            $.ajax({
                url: "/sign/",
                // contentType: 'application/json',
                type: 'POST',
                data: post_data,
                success: function (data) {
                    console.log(data)
                    result = JSON.stringify(data)
                    if (result['status'] === 200){
                        location.href = '/home/'
                    }
                    else {
                        location.href = '/sign/'
                    }
                },
                fail: function (result) {
                    console.log('失败');
                }
            });
        }

        return check;
    });



    $('.validate-form .input-content').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });

    function validate(input) {
        if ($(input).attr('type') === 'text') {
            // 用户名：4-16位字母,数字,汉字,下划线
            if ($(input).val().match(/^[a-zA-Z0-9_\u4e00-\u9fa5]{4,16}$/) == null) {
                console.log($(input).val())
                alert("用户名不合法！\n用户名由汉字、字母、数字、下划线组成，长度为4-16位！");
                return false;
            }
        } else if ($(input).attr('type') === 'password') {
            // 密码：包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位
            if ($(input).val().match(/^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$/) == null) {
                alert("密码格式不合法！\n密码包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符，最少6位！");
                return false;
            }
        } else {
            if ($(input).val().trim() === '') {
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

})(jQuery);
