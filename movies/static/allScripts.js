$(function() {
    $('#idselect').val('all');
});

$("#searchShowHide").click(function () {
    $("#searchBarUp").toggleClass('hideSearchBar showSearchBar');
});

onSearchChangeHe = () => {
    $(".searchDD").val()=="all" ?
    $("div > div input.sInput")[0].placeholder="חפש...":
    $(".searchDD").val()=="title" ?
    $("div > div input.sInput")[0].placeholder="[שם הסרט]":
    $(".searchDD").val()=="year" ?
    $("div > div input.sInput")[0].placeholder="[שנה]-[שנה]/[שנה]":
    $(".searchDD").val()=="director" ?
    $("div > div input.sInput")[0].placeholder="[שם במאי]": $(".sInput")[0].placeholder="erroe";
}

onSearchChange = () => {
    $(".searchDD").val()=="all" ?
    $("div > div input.sInput")[0].placeholder="Search...":
    $(".searchDD").val()=="title" ?
    $("div > div input.sInput")[0].placeholder="[Title]":
    $(".searchDD").val()=="year" ?
    $("div > div input.sInput")[0].placeholder="[Year]-[Year]/[Year]":
    $(".searchDD").val()=="director" ?
    $("div > div input.sInput")[0].placeholder="[Director's name]": none;
}