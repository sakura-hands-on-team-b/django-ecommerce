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

    if ($('.card-add').length) {
      $('.card-add').on('click',function(){
        let productId = $(this).attr('product_id');
        let quantity = 1;
        if ($('#quantity-'+productId).length) {
          quantity = $('#quantity-'+productId).val();
        }
        let url= `/ec/cart_add/${productId}?quantity=${quantity}`;
        location.href= url;
      });
    }
});
