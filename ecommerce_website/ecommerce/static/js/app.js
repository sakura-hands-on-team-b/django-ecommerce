var app = app || {};
app.isLoading = false;


$(function(){
    
    if ($('.on-datepicker').length >0) {
        $('.on-datepicker').datetimepicker({
            dayViewHeaderFormat: 'YYYY MM',
            format: 'YYYY/MM/DD',
            locale: 'ja',
            stepping: 1,
            showTodayButton: true
            
        });
    }
    if ($('.on-timepicker').length >0) {
        $('.on-timepicker').datetimepicker({
            format: 'HH:mm:ss',
            locale: 'ja',
            stepping: 1,
            showTodayButton: true
            
        });
    }
});