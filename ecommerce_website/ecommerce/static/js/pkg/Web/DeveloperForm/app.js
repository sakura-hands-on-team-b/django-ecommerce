var app = app || {};
app.isLoading = false;


$(function(){
    
    if ($('#developer-edit').length) {
        $('#developer-edit').off('click').on('click',function(){
            app.moveDeveloperForm();
        });
    }
    
    if ($('#search-list-form-btn').length) {
        $('#search-list-form-btn').on('click',function(){
            console.log($('#search-list-form-btn').hasClass('active'));
            if ($('#search-list-form-btn').hasClass('active')) {
                $('#search-list-form-btn').removeClass('active');
                $('#search-list-form').addClass('hide');
            } else {
                $('#search-list-form-btn').addClass('active','active');
                $('#search-list-form').removeClass('hide');
            }
        });
    }
    if ($('#slack-addr-chk').length && $('#mail-addr-chk').length) {
        $('#slack-addr-chk,#mail-addr-chk').off('click').on('click',function(){
            app.toggleAddrInput(this);
        });
    }
    
    if ($('#create-body').length) {
        $('#create-body').off('click').on('click',function(){
            app.createBody();
        });
        
    }
    if ($('#begin_date').length) {
        $('#begin_date').on('focusout',function(){
            if (!$('#end_date').val()) {
                $('#end_date').val($('#begin_date').val());
            }
        });
    }
    if ($('#project_name').length) {
        $('#project_name').on('focusout',function(){
            if (!$('#title').val()) {
                $('#title').val($('#project_name').val());
            }
        });
    }
});

app.moveDeveloperForm = function(){
    if ($('#developer_id').length) {
        let id = $('#developer_id').val();
        if (id) {
            location.href = `${urlBase}developer/form/${id}`;
        }
    }
};

app.toggleAddrInput = function(obj) {
    let id = $(obj).attr('id');
    let targetId = id.substr(0,id.length-4);
    console.log($(obj));
    if ($(obj).prop('checked')) {
        $('#'+targetId).attr('readonly','readonly');
    } else {
        $('#'+targetId).removeAttr('readonly');
    }
}

app.createBody = function() {
    let request = window.superagent;
    if (!app.isCreateBodyValid()) {
        return false;
    }
    request
        .post(`${urlBase}releasepost/body/template`)
        .type('form')   // encodeをさぼる
        .send({"schedule_begin_date": $('#begin_date').val()})
        .send({"schedule_begin_time": $('#begin_time').val()})
        .send({"schedule_end_date": $('#end_date').val()})
        .send({"schedule_end_time": $('#end_time').val()})
        .send({"project_name": $('#project_name').val()})
        .send({"server_names": $('#server_names').val()})
        .end(function(err,res){
            if (!res.ok || !res.body.body) {
                alert('通信エラー');
                return false;
            }
            $('#body').text(res.body.body);
            $('#body').removeClass('hide');
            return false;
        });
    return false;
}

app.isCreateBodyValid = function()
{
    let isValid = true;
    if (!$('#begin_date').val()) {
        alert('開始日が入力されていません');
        isValid = false;
    }
    if (!$('#begin_time').val()) {
        alert('開始時間が入力されていません');
        isValid = false;
    }
//    if (!$('#end_date').val()) {
//        alert('終了予定日が入力されていません');
//        isValid = false;
//    }
    if (!$('#end_time').val()) {
        alert('終了予定時間が入力されていません');
        isValid = false;
    }
    if (!$('#project_name').val()) {
        alert('プロジェクト名が入力されていません');
        isValid = false;
    }
//    if ($('#server_name').val()) {
//        alert('サーバ名が入力されていません');
//        isValid = false;
//    }
    return isValid;
}