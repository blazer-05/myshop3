function getCookie(name) {
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function renderCartTemplate(data) {
    var tmpl = '<div class="top-cart">' +
    '    <ul>' +
    '        <li>' +
    '            <a href="/cart/">' +
    '                <span class="cart-icon"><i class="fa fa-shopping-cart"></i></span>' +
    '                <span class="cart-total">' +
    '                <span class="cart-title">Shopping cart</span>' +
    '                <span class="cart-item" id="cart_count">' + data.count + ' item(s)- </span>' +
    '                <span class="top-cart-price cart-total-price">$' + data.total +'</span>' +
    '                </span>' +
    '            </a>' +
    '            <div class="mini-cart-content">';
    var products = data.products;
    products.forEach(function(product, i, products){

    tmpl = tmpl +
    '                <div class="cart-img-details">' +
    '                    <div class="cart-img-photo">' +
    '                        <a href="' + product.url +'">' +
    '                            <img src="' + product.images + '" alt="' + product.title + '">' +
    '                        </a>' +
    '                    </div>' +
    '                <div class="cart-img-content">' +
    '                    <a href="' + product.url + '"><h4>' + product.title + '</h4></a>' +
    '                    <span>' +
    '                        <strong class="text-right">' + product.quantity + ' x</strong>' +
    '                        <strong class="cart-price text-right">$' + product.price + '</strong>' +
    '                    </span>' +
    '                </div>' +
    '                <div class="pro-del">' +
    '                    <a href="" class="remove_from_cart" onclick="return removeFromCart(\'' + product.slug + '\')">' +
    '                        <i class="fa fa-times"></i>' +
    '                    </a>' +
    '                </div>' +
    '            </div>'
    });
    tmpl = tmpl +
    '            <div class="clear"></div>' +
    '            <div class="cart-inner-bottom">' +
    '                <span class="total">' +
    '                    TOTAL:' +
    '                    <span class="amount cart-total-price">$' + data.total + '</span>' +
    '                </span>' +
    '                <span class="cart-button-top">' +
    '                    <a href="/cart/">View cart</a>' +
    '                    <a href="checkout.html">Checkout</a>' +
    '                </span>' +
    '            </div>' +
    '        </div>' +
    '    </li>' +
    '</ul>' +
    '</div>';
    return tmpl;
}

function renderCartTableTemplate(data) {
    var products = data.products;
    if(products.length == 0)
      return '<h3 class="text-left"><strong>Your basket is empty</strong></h3>';

    var tmpl = '' +
      '<div class="table-responsive">' +
      '    <table class="table table-bordered table-hover bmw">' +
      '        <thead>' +
      '            <tr>' +
      '                <td class="text-center">Image</td>' +
      '                <td class="text-left">Product Name</td>' +
      '                <td class="text-center">Quantity</td>' +
      '                <td class="text-right">Unit Price</td>' +
      '                <td class="text-right">Total</td>' +
      '            </tr>' +
      '        </thead>';


    products.forEach(function(product, i, products) {
        tmpl = tmpl +
          '        <tbody>' +
          '            <tr class="cart-item-">' +
          '                <td class="text-center">' +
          '                    <a href="' + product.url + '">' +
          '                        <img class="img-thumbnail" src="' + product.thumb + '" alt="' + product.url + '" />' +
          '                    </a>' +
          '                </td>' +
          '                <td class="text-left">' +
          '                    <a href="' + product.url + '">' + product.title + '</a>' +
          '                </td>' +
          '                <td class="text-center">' +
          '                    <form class="product-quantity" onsubmit="return changeCart(event)">' +
          '                        <div style="display: inline-block; width: 110px">' +
          '                            <div class="input-group plus-minus-widget">' +
          '                                <span class="input-group-btn">' +
          '                                    <button class="btn btn-default" type="submit" style="width: 35px" onclick="quantityChange(event, -1)">-</button>' +
          '                                </span>' +
          '                                <input type="text" placeholder="1" value="' + product.quantity + '" name="quantity" class="form-control">' +
          '                                <span class="input-group-btn">' +
          '                                    <button class="btn btn-default" type="submit" style="width: 35px" onclick="quantityChange(event, +1)">+</button>' +
          '                                </span>' +
          '                            </div>' +
          '                        </div>' +
          '                        <input type="hidden" name="product" value="' + product.slug + '"/>' +
          '                    </form>' +
          '                    <div style="display: inline-block;">' +
          '                        <div class="input-group">' +
          '                            <button class="btn btn-danger" title="Remove" onclick="return removeFromCartTable(event, \'' + product.slug + '\')"><i class="fa fa-times-circle"></i></button>' +
          '                        </div>' +
          '                    </div>' +
          '                </td>' +
          '                <td class="text-right" id="cart-item-total-">&#8381; ' + product.price + '</td>' +
          '                <td class="text-right" id="cart-item-total-">&#8381; ' + product.total + '</td>' +
          '            </tr>' +
          '        </tbody>';
    });

    tmpl = tmpl +
      '    </table>' +
      '</div>';

    tmpl = tmpl +
      '<div class="row" id="hide">' +
      '    <div class="col-sm-4 col-sm-offset-8">' +
      '        <table class="table table-bordered">' +
      '            <tbody>' +
      '                <tr>' +
      '                    <td class="text-right">' +
      '                        <strong>Total:</strong>' +
      '                    </td>' +
      '                    <td class="text-right cart-total-price"><strong>&#8381; ' + data.total + ' </strong></td>' +
      '                </tr>' +
      '            </tbody>' +
      '        </table>' +
      '    </div>' +
      '</div>';
    return tmpl;
}

function cartInfo() {
  const url = '/cart/info/';
  fetch(url)
    .then(function (res) {
      res.json().then(function (res) {
        $('#cart-info').html(renderCartTemplate(res));
        if(window.location.pathname == '/cart/') {
          cartTableInfo(res);
        }
      })
    });
}

function cartTableInfo(res) {
  $('#cart-table').html(renderCartTableTemplate(res));
}

function addToCart(e) {
  const url = '/cart/add/';
  let data = new FormData(e.target);
  const content = fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: data
  }).then(function(res){

    var that = $(e.target).closest('.row').find('img');
    var bascket = $(".top-cart");
    var w = that.width();
    that.clone()
        .css({'width' : w,
        'position' : 'absolute',
        'z-index' : '9999',
        top: that.offset().top,
        left:that.offset().left})
        .appendTo("body")
        .animate({opacity: 0.05,
            left: bascket.offset()['left'],
            top: bascket.offset()['top'],
            width: 50}, 1000, function() {
                $(this).remove();
            });

    cartInfo()
  });
  return false
}
function removeFromCart(productSlug, callback) {
  const url = '/cart/remove/';
  let data = new FormData();
  data.append("product", productSlug);
  const content = fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: data
  }).then(function(res){
    cartInfo();
    if(callback !== undefined)
        callback()
  });
  return false;
}
function changeCart(e) {
  const url = '/cart/change/';
  let data = new FormData(e.target);
  const content = fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: data
  }).then(function(res){
    cartInfo()
  });
  return false;
}
function removeFromCartTable(e, productSlug) {
  removeFromCart(productSlug)
}

function quantityChange(e, action) {
    let widget = $(e.target).closest('.plus-minus-widget');
    let field = widget.find('input');
    let value = parseInt(field.val());
    if(isNaN(value))
        value = 1;
    value = value + action;
    value = value < 1 ? 1 : value;
    field.val(value)
}

cartInfo();