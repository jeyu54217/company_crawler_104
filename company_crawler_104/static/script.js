// datatable
 $(document).ready(function() {
    $('#datatable').DataTable();
});

//  search-table
$('#addRowChild').click(function(){
    // window.alert('GO!');
    $('#search-table tbody').append(`<tr>${$('#default-row').html()}</tr>`);
});

$('#btn_search_submit').click(function(){
    // get all keyword value from html class name
    var kwyword_ary = Array();
    kwyword_ary.push($('.form-control').map(function(){
        return this.value
    }).get());

    var data_for_post = {
        'key_of_kwyword_list[]' : kwyword_ary  // must add [] as key
    };

    var post_search_data = $.post('http://127.0.0.1:8000/search/', data_for_post);
    // redirect current page
    $.when(post_search_data).done(function(){
        window.location.href="http://127.0.0.1:8000/search/";
    });
 });


 $('#btn_csv_submit').click(function(){

    var btn_csv_submit = $.post('http://127.0.0.1:8000/csv_insert/');

 });


 $('#btn_Save').click(function(){
    var checked_ary = Array();
    var note_id_ary = Array();
    var note_value_ary = Array();
    // var output_path_arr = Array();  

    checked_ary.push($('[name^="checkbox_"]:checked').map(function(){
        return $(this).attr('name')
    }).get());

    note_id_ary.push($('[name^="text_"]').map(function(){ 
        return $(this).attr('name')
    }).get());

    note_value_ary.push($('[name^="text_"]').map(function(){ 
        return this.value
    }).get());

    // output_path_arr.push($('[name^="output-path"]').map(function(){ 
    //     return this.value
    // }).get());

    var data_for_post_ = {
        'key_of_checked_list[]' : checked_ary,
        'key_of_note_id_list[]' : note_id_ary,
        'key_of_note_value_list[]' : note_value_ary,
        // 'key_of_output_path[]' : output_path_arr,
    };

    var post_checked_data = $.post('http://127.0.0.1:8000/save/', data_for_post_);
         // redirect current page
    // $.when(post_checked_data).done(function(){
    //     window.location.href="http://127.0.0.1:8000/"
    // });
});

$('#btn_Mapping').click(function(){
    var checked_ary = Array();
    var note_id_ary = Array();
    var note_value_ary = Array();
    // var output_path_arr = Array();  

    checked_ary.push($('[name^="checkbox_"]:checked').map(function(){
        return $(this).attr('name')
    }).get());

    note_id_ary.push($('[name^="text_"]').map(function(){ 
        return $(this).attr('name')
    }).get());

    note_value_ary.push($('[name^="text_"]').map(function(){ 
        return this.value
    }).get());

    // output_path_arr.push($('[name^="output-path"]').map(function(){ 
    //     return this.value
    // }).get());

    var data_for_post_ = {
        'key_of_checked_list[]' : checked_ary,
        'key_of_note_id_list[]' : note_id_ary,
        'key_of_note_value_list[]' : note_value_ary,
        // 'key_of_output_path[]' : output_path_arr,
    };

    var post_checked_data = $.post('http://127.0.0.1:8000/save/', data_for_post_);
    var post_mapping_triger = $.post('http://127.0.0.1:8000/mapping/');
         // redirect current page
    $.when(post_mapping_triger).done(function(){
        window.location.href="http://127.0.0.1:8000/mapping/"
    });
});

$('#btn_excel_submit').click(function(){
    var update_ary = Array();
    var output_path_arr = Array();  

    update_ary.push($('[name^="input_id"]').map(function(){
        return this.value
    }).get());

    output_path_arr.push($('[name^="output-path"]').map(function(){ 
        return this.value
    }).get());

    var data_for_post_ = {
        'key_of_update_ary[]' : update_ary,
        'key_of_output_path[]' : output_path_arr,
    };

    var post_update_data = $.post('http://127.0.0.1:8000/update_mapping/', data_for_post_);
    // var post_mapping_triger = $.post('http://127.0.0.1:8000/select_to_excel/');
         // redirect current page
    // $.when(post_checked_data).done(function(){
    //     window.location.href="http://127.0.0.1:8000/"
    // });
});
