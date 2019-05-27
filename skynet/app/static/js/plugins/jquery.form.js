/*!
 * 表单实用函数
 * @author shajunxing
 * @version 0.0.0.0
 */

(function ($) {
    /**
     * 将表单中的输入控件的值转换成键值对对象的格式，以下是转换规则：
     * 1. 文本框(type=text, type=password)、文本区域、不包含multiple属性的下拉选择框、name相同的一组单选框转换为字符串
     *    注意：一组单选框如果都没有点选，则为null
     * 2. 数值类型的文本框(type=number)转换为数字(HTML5 Only)
     * 3. 不包含value属性的复选框转换为布尔值
     *    注意：不应该出现多个name相同而又不包含value属性的复选框，否则结果不可预料
     * 4. name相同且都包含value属性的复选框、包含multiple属性的多重选择框(按ctrl键多选)的所选项转换为字符串数组
     *    注意：当前只能转成字符串数组
     * @return {*}
     */
    $.fn.getFormValueToJson = function () {
        var ret = {};

        // 文本类型
        this.find('input[type=text], input[type=password], textarea, select:not([multiple])').each(function () {
            var name = $(this).prop('name');
            ret[name] = $(this).val();
        });

        this.find('input[type=radio]').each(function () {
            var name = $(this).prop('name');
            if (!ret[name]) {
                ret[name] = null;
            }
            if ($(this).prop('checked')) {
                ret[name] = $(this).prop('value');
            }
        });

        // 数值类型
        this.find('input[type=number]').each(function () {
            var name = $(this).prop('name');
            ret[name] = Number($(this).val());
        });

        // 布尔类型
        this.find('input[type=checkbox]:not([value])').each(function () {
            var name = $(this).prop('name');
            ret[name] = $(this).prop('checked');
        });


        // 数组
        this.find('select[multiple]').each(function () {
            var name = $(this).prop('name');
            ret[name] = $(this).val() || [];
        });

        this.find('input[type=checkbox][value]').each(function () {
            var name = $(this).prop('name');
            if (!ret[name]) {
                ret[name] = [];
            }
            if ($(this).prop('checked')) {
                ret[name].push($(this).prop('value'))
            }
        });

        return ret;
    };

    /**
     * getValue的逆操作，设置符合类型的控件的值
     * @param val
     */
    $.fn.setFormValueFromJson = function (val) {
        // 文本类型
        this.find('input[type=text], input[type=password], textarea, select:not([multiple])').each(function () {
            var name = $(this).prop('name');
            if (val[name] && typeof(val[name]) == 'string') {
                $(this).val(val[name]);
            }
        });

        this.find('input[type=radio]').each(function () {
            var name = $(this).prop('name');
            if (val[name] && typeof(val[name]) == 'string' && $(this).prop('value') == val[name]) {
                $(this).prop('checked', true);
            }
        });

        // 数值类型
        this.find('input[type=number]').each(function () {
            var name = $(this).prop('name');
            if (val[name] && typeof(val[name]) == 'number') {
                $(this).val(val[name]);
            }
        });

        // 布尔类型
        this.find('input[type=checkbox]:not([value])').each(function () {
            var name = $(this).prop('name');
            if (val[name] && typeof(val[name]) == 'boolean') {
                $(this).prop('checked', val[name]);
            }
        });


        // 数组
        this.find('select[multiple]').each(function () {
            var name = $(this).prop('name');
            if (val[name] && val[name] instanceof Array) {
                $(this).val(val[name])
            }
        });

        this.find('input[type=checkbox][value]').each(function () {
            var name = $(this).prop('name');
            if (val[name] && val[name] instanceof Array && $(this).prop('value') in val[name]) {
                $(this).prop('checked', true);
            }
        });
    };

}(jQuery));