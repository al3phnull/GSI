function onOffSubMenu() {
  var menuElem = document.getElementById('sweeties');
  var titleElem = document.getElementById('title');

  titleElem.onclick = function() {
    $('#icon_static').toggleClass("fa-chevron-right", "fa-chevron-down");
    $('#icon_static').toggleClass("fa-chevron-down", "fa-chevron-right");
    $('#sweeties').toggleClass("sub-menu-visible", "sub-menu-no-visible");
    $('#sweeties').toggleClass("sub-menu-no-visible", "sub-menu-visible");
  };
}

function onOffSubMenuUser() {
  var menuElem = document.getElementById('dropUser');
  var titleElem = document.getElementById('titleUser');

  titleElem.onclick = function() {
    menuElem.classList.toggle('open');
    $(".icon-visible-user").toggle();
    document.getElementById("dropdownUser").classList.toggle("show");
  };
}

function showSubMenuUser() {
  document.getElementById("dropdownUser").classList.toggle("show");
}

function invisibleDropMenu() {
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn-user')) {
      var dropdowns = document.getElementsByClassName("dropdown-content-user");
      var i;
      event = event || window.event;
      var target = event.target || event.srcElement;

      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];

        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
          $(".icon-visible-user").toggle();
        }
      }
    }
  }
}

function invisibleSelect() {
  $("select").selecter();
  //$("select").dropdown();
}

function changeColorError() {
  if ( $('span').is('.field-error') ) {
    $('span.field-error > .form-control').toggleClass('field-error');
    $('span.field-error > div.selecter > .selecter-selected').toggleClass('field-error');
  }
}

function changeColorSuccess() {
  var elems = $('div .form-control');
  var elemsTotal = elems.length;

  for(var i = 0; i < elemsTotal; ++i){
    if ($(elems[i]).val()){
      $(elems[i]).toggleClass('field-success');
    }
  }
}

function colorBlackSelect() {
  var select_item = $('span.selecter-selected');
  var select_total = select_item.length;

  for(var i = 0; i < select_total; ++i) {
    var select_text = $(select_item[i]).text();

    if (select_text.indexOf('Select') < 0){
      $(select_item[i]).toggleClass('color-222');
      $(select_item[i]).toggleClass('field-success');
    } else {
      $(select_item[i]).toggleClass('color-999');
      $(select_item[i]).removeClass('field-success');
    }
  }
}

function selectAllAvialable() {
  $('#select-available-files option').each(function(){
    $('div.available div.multiple select option').attr("selected", "selected");
    $('div.available div.multiple div.selecter-options span.selecter-item').attr("class", "selecter-item selected");
  });
}

function selectAllChosen() {
  $('#select-chosen-files option').each(function(){
    $('div.chosen div.multiple select option').attr("selected", "selected");
    $('div.chosen div.multiple div.selecter-options span.selecter-item').attr("class", "selecter-item selected");
  });
}

function visibleDoy(){
  var doyElement = $('span.field-success').html();

  if (doyElement === 'Input a variable'){
    $(".doy-label").removeClass("disabled");
    $(".doy").removeClass("disabled");
    $(".doy-label").addClass("visible");
    $(".doy").addClass("visible");
  } else {
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");
  };
}

function statusPeriod(){
  var periodElement = $('span.field-success').html();

  if (periodElement === 'Input a variable'){
    $(".doy").removeClass("disabled");
    $(".doy-label").removeClass("disabled");
    $(".doy").addClass("visible");
    $(".doy-label").addClass("visible");
  } else {
    $(".doy").removeClass("visible");
    $(".doy-label").removeClass("visible");
    $(".doy").addClass("disabled");
    $(".doy-label").addClass("disabled");
  };
}

function getRandomArbitary(min, max)
{
  return Math.random() * (max - min) + min;
}

function addRunCardItem(){
  var select = $("#carditem_all option:selected").text();
  var select_val = $("#carditem_all option:selected").val();
  var order = $("input#order_carditem").val();
  var id_str = new String(getRandomArbitary(1, 10000)).replace(/\./g, "");
  var indetificator = Number(id_str);
  //alert('1 indetificator = '+indetificator);
  //alert('Select VAL = '+select_val);
  //alert('Select TXT = '+select);
  //alert('Order VAL = '+order);

  $("tbody").append('<tr id="'+indetificator+'"></tr>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'"><input type="checkbox" name="carditem_select" value="'+select_val+'" class="select_item" checked></td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'">'+select+'</td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'" name="carditem_order"><input type="text" class="center non-input" name="carditem_order" value="'+order+'" class="select_item"</td>');
  $("tbody > tr#"+indetificator).append('<td class="'+indetificator+'"><button class="btn del-btn check-cur-delete" type="button" name="del_current_btn" value="'+indetificator+'" onclick="deleteCurrentCardItem('+indetificator+')"><img src="/static/img/delete-18.png"/></button></td>');
  //alert('2 indetificator = '+indetificator);
}

function deleteCurrentCardItem(item){
  //alert('deleteCurrentCardItem = '+item);
  var name = new String(item);
  //alert('TAG = '+$("tr#"+item));

  $("tr#"+item).detach();
  $("td."+item).detach();
}


$(document).ready(function(){
  //selectAll();
  onOffSubMenu();
  invisibleDropMenu();
  onOffSubMenuUser();
  invisibleSelect();
  changeColorError();
  changeColorSuccess();
  colorBlackSelect();
  statusPeriod();
});