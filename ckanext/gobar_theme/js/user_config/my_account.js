$(function () {
    var showEditSection = function (e) {
        var replaceId = $(e.currentTarget).parents('.disabled-input').addClass('hidden').data('replace-id');
        $('#' + replaceId).removeClass('hidden');
        clearFeedback($(e.currentTarget).siblings('input'))
    };
    $('.disabled-input svg').click(showEditSection);


    var resetEditSection = function (editSection) {
        var inputs = editSection.find('input');
        for (var i=0; i<inputs.length; i++) {
            var $input = $(inputs[i]);
            $input.val($input.data('default-value') || '');
            clearFeedback($input);
        }
        editSection.addClass('hidden')
        return $('div[data-replace-id="' + editSection.attr('id') + '"]').removeClass('hidden');
    };
    $('#cancel-email, #cancel-password').click(function (e) {
        var editSection = $(e.currentTarget).parents('.edit-section');
        resetEditSection(editSection);
    });


    var sendChanges = function (editSection) {
        var inputs = editSection.find('input');
        var endpoint = editSection.data('endpoint');
        var data = {};
        var newData = $(inputs[1]).val();
        var attr = editSection.data('attr');
        data[attr] = newData;
        if (attr == 'password') {
            data['current-' + attr] = $(inputs[0]).val();
        }
        var button = editSection.find('#save-email, #save-password');
        button.prop('disabled', true);
        var callback = function (response) {
            button.prop('disabled', false);
            var attr = editSection.data('attr');
            if(response.success) {
                var defaultSection = resetEditSection(editSection);
                var input = defaultSection.find('input')
                input.val(newData)
                if (attr == 'password') {
                    showPositiveFeedback(input, 'Your password has been changed.')
                } else {
                    showPositiveFeedback(input, 'Succesfully changed your e-mail.')
                }
            } else {
                if (attr == 'password' && response.error == 'current_password') {
                    showNegativeFeedback($(inputs[0]), 'This is not your current password. Please try again!!!');
                } else {
                    var secondInput = $(inputs[2]);
                    clearFeedback(secondInput);
                    showNegativeFeedback(firstInput, 'An error occurred.');
                }
            }
        };
        var failCallback = function () { button.prop('disabled', false); }
        $.post(endpoint, data, callback).fail(failCallback);
    };

    var validate = function (editSection) {
        var inputs = editSection.find('input');
        var firstInput = $(inputs[1]);
        var secondInput = $(inputs[2]);
        var valuesAreEqual = firstInput.val() == secondInput.val();

        clearFeedback($(inputs[0]));
        clearFeedback(firstInput);
        clearFeedback(secondInput);

        if (firstInput.val().length == 0) {
            showNegativeFeedback(firstInput, 'Please complete required data.');
            return false
        }

        if (secondInput.val().length == 0) {
            showNegativeFeedback(secondInput, 'Please complete required data.');
            return false
        }

        var attr = editSection.data('attr');

        if (!valuesAreEqual) {
            if (attr == 'password') {
                showNegativeFeedback(firstInput, '');
                showNegativeFeedback(secondInput, 'Oh! Passwords do not match. Try again.');
            } else {
                showNegativeFeedback(firstInput, '');
                showNegativeFeedback(secondInput, 'Oh! The emails do not match. Try again.');
            }
            return false
        }

        if (attr == 'password' && secondInput.val().length < 4) {
            showNegativeFeedback(secondInput, 'Use at least 4 characters.');
            return false
        } else if (attr == 'email') {
            if (!email_re.test(secondInput.val())) {
                showNegativeFeedback(secondInput, 'Use this format name@example.com.');
                return false;
            }
        }
        return true
    };

    $('#save-email, #save-password').click(function (e) {
        var editSection = $(e.currentTarget).parents('.edit-section');
        var isValid = validate(editSection);
        if (isValid) {
            sendChanges(editSection)
        }
    });
});
