/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/


// Set session variables
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// Call stripe variables
var stripe = Stripe(stripePublicKey);


// Set appearance and options
const appearance = {
  theme: 'flat',
  variables: { colorPrimaryText: '#262626' }
};
const options = {
  layout: {
    type: 'tabs',
    defaultCollapsed: false,
  }
};

// Mount card element to div
const elements = stripe.elements({ clientSecret, appearance });
var card = elements.create('card', options);
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // prevent default action
    ev.preventDefault();

    // Disable card element and submit while code is running, preventing multiple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // Pass card details to Stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {

        // If error, display message
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // Re-enable card element & submit to allow user to try again
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
            
        } else {
            // If success, submit form
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});

// Show a spinner on payment submission - NEEDS IMPLEMENTING

// function setLoading(isLoading) {
//   if (isLoading) {
//     // Disable the button and show a spinner
//     document.querySelector("#submit").disabled = true;
//     document.querySelector("#spinner").classList.remove("hidden");
//     document.querySelector("#button-text").classList.add("hidden");
//   } else {
//     document.querySelector("#submit").disabled = false;
//     document.querySelector("#spinner").classList.add("hidden");
//     document.querySelector("#button-text").classList.remove("hidden");
//   }
// }