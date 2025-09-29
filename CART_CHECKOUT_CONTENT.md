# Cart & Checkout Content

## 1. Shopping Cart Page (/cart/)

### Page Title
**"Your Shopping Cart"**

### Empty Cart State

#### Headline
**"Your cart is empty"**

#### Subheadline
**"Looks like you haven't added anything to your cart yet"**

#### CTA
**"Continue Shopping"** → Links to /shop/

#### Suggestions
**"You might like these popular items:"**
- Display 4 trending products
- Quick add to cart functionality

---

### Active Cart State

#### Cart Summary Header
**"Shopping Cart (3 items)"**

#### Security Message
**"🔒 Secure Checkout - Your information is protected with 256-bit SSL encryption"**

#### Item Display Format
```
[Product Image] | Product Name | Size: M | Color: Black | Qty: [- 1 +] | ₹649 | [Remove]
```

#### Cart Actions
- **"Save for Later"** - Move to wishlist
- **"Remove"** - Delete from cart
- **"Edit"** - Change size/color

#### Cart Summary Sidebar
```
Order Summary
─────────────
Subtotal (3 items):     ₹1,947
Shipping:              FREE
Discount (WELCOME10):  -₹195
─────────────
Total:                 ₹1,752

✅ You saved ₹195 today!
```

#### Shipping Information
- **Free Shipping** on orders above ₹999 ✅
- **Standard Delivery:** 3-5 business days
- **Express Delivery:** +₹99 for 1-2 business days

#### Promo Code Section
**"Have a promo code?"**
- Input field for code
- **"Apply"** button
- Display applied discounts

#### Trust Elements
- **🔒 Secure Payment** - SSL Encrypted
- **📦 Free Shipping** - On orders ₹999+
- **↩️ Easy Returns** - 30-day policy
- **💬 24/7 Support** - Help when you need it

#### Primary CTAs
- **"Proceed to Checkout"** - Primary button
- **"Continue Shopping"** - Secondary link

---

## 2. Checkout Process

### 2.1 Checkout Header
**"Secure Checkout"** with progress indicator:
**Shipping → Payment → Confirmation**

### 2.2 Guest vs Account Checkout
**"Checkout as Guest or Create Account for faster future purchases"**
- **"Checkout as Guest"** - Quick option
- **"Create Account"** - With benefits list
- **"Already have an account? Sign In"** - Login link

---

## 3. Shipping Information Page (/checkout/shipping/)

### Page Title
**"Shipping Information"**

### Form Fields
```
Contact Information
- Email Address*
- Phone Number*

Shipping Address
- Full Name*
- Address Line 1*
- Address Line 2 (Optional)
- City*
- State*
- PIN Code*
- Address Type: Home / Office / Other
```

### Address Book (For Logged Users)
**"Choose from saved addresses"**
- Radio button selection
- **"Add New Address"** option

### Delivery Options
```
📦 Standard Delivery (3-5 business days) - FREE
🚀 Express Delivery (1-2 business days) - ₹99
```

### Order Summary (Sidebar)
- Collapsed view of cart items
- Total amount
- Estimated delivery date

### Navigation
- **"Back to Cart"** - Secondary link
- **"Continue to Payment"** - Primary CTA

---

## 4. Payment Information Page (/checkout/payment/)

### Page Title
**"Payment Information"**

### Security Message
**"🔒 Your payment information is secure and encrypted"**

### Payment Methods

#### Credit/Debit Cards
```
💳 Credit/Debit Card
- Card Number
- Expiry Date (MM/YY)
- CVV
- Cardholder Name
```

#### Digital Wallets
```
📱 Digital Wallets
- 🎯 Paytm
- 📱 PhonePe
- 💙 Google Pay
- 🍎 Apple Pay
```

#### Net Banking
```
🏛️ Net Banking
- Select Your Bank (Dropdown)
```

#### UPI
```
📲 UPI
- Enter UPI ID
- Quick UPI Apps: GPay, PhonePe, Paytm
```

#### Cash on Delivery
```
💰 Cash on Delivery
- Available for orders under ₹5,000
- Additional charges: ₹49
```

### Billing Address
**"Billing address same as shipping address"** ✅
- Option to use different billing address

### Order Summary
```
Order Total: ₹1,752
Payment Method: Credit Card
Delivery: Standard (3-5 days)
```

### Terms & Conditions
**"By placing this order, you agree to our Terms & Conditions and Privacy Policy"**

### Primary CTA
**"Place Order"** - Complete purchase button

---

## 5. Order Confirmation Page (/checkout/confirmation/)

### Success Message
**"🎉 Order Placed Successfully!"**

### Order Details
```
Order Number: #ORD-2025-001234
Order Date: September 29, 2025
Total Amount: ₹1,752
Payment Method: Credit Card ending in ****1234
```

### Delivery Information
```
Estimated Delivery: October 2-4, 2025
Shipping Address:
[Customer Address]
```

### Order Items
List of purchased items with images and details

### What's Next
**"What happens next?"**
1. **Order Confirmation** - You'll receive an email confirmation
2. **Order Processing** - We'll prepare your items (1-2 business days)
3. **Shipping** - Your order will be dispatched
4. **Delivery** - Track your package until it reaches you

### Action Buttons
- **"Track Your Order"** → Order tracking page
- **"Continue Shopping"** → Homepage
- **"Print Receipt"** → PDF download

### Customer Support
**"Need help with your order?"**
- **"Contact Support"** - Link to contact page
- **"Call us:** 1800-XXX-XXXX
- **"WhatsApp:** +91-XXXXX-XXXXX

---

## 6. Order Tracking Page (/orders/track/<order_id>/)

### Page Title
**"Track Your Order"**

### Order Status Timeline
```
✅ Order Placed (Sep 29, 2025, 2:30 PM)
✅ Payment Confirmed (Sep 29, 2025, 2:31 PM)
🔄 Order Processing (Sep 30, 2025, 10:00 AM)
📦 Order Shipped (Pending)
🚚 Out for Delivery (Pending)
✅ Delivered (Pending)
```

### Tracking Information
```
Order Number: #ORD-2025-001234
Tracking ID: TRK123456789
Estimated Delivery: October 2-4, 2025
Shipping Partner: Blue Dart
```

### Live Tracking
**"Track with shipping partner"** → External tracking link

### Order Details
- Items ordered
- Shipping address
- Payment information

---

## 7. Cart Abandonment Elements

### Exit Intent Popup
**"Wait! Don't miss out on these amazing products"**
- **"Complete your purchase and get 5% off"**
- Discount code: SAVE5NOW
- **"Complete Purchase"** CTA

### Reminder Emails
**Subject:** "You left something in your cart"
**Content:** "Your cart is waiting for you. Complete your purchase before items go out of stock."

---

## 8. Trust & Security Elements

### Security Badges
- **SSL Certified** - 256-bit encryption
- **PCI DSS Compliant** - Secure payments
- **Verified by Visa** - Card security
- **Mastercard SecureCode** - Additional protection

### Money-Back Guarantee
**"100% Money-Back Guarantee"**
- 30-day return policy
- Full refund if not satisfied
- No questions asked

### Customer Testimonials
**"What our customers say about shopping with us:"**

- **"Safe and secure checkout"** - Priya S.
- **"Quick delivery and great quality"** - Sneha M.
- **"Trusted brand, hassle-free returns"** - Kavya R.

---

## 9. Mobile Cart & Checkout Optimization

### Mobile Cart Features
- **Sticky total bar** at bottom
- **Swipe to remove** items
- **Quick quantity adjust** with +/- buttons
- **One-thumb navigation**

### Mobile Checkout
- **Single-page checkout** option
- **Auto-fill** address suggestions
- **Touch-optimized** payment forms
- **Mobile wallet** quick pay

### Progressive Web App Features
- **Save cart** offline
- **Push notifications** for abandoned carts
- **Quick checkout** from home screen

---

## 10. Error Handling & Messages

### Common Error Messages

#### Out of Stock
**"Sorry, this item is currently out of stock"**
- **"Notify me when available"** option
- **"View similar products"** suggestions

#### Invalid Promo Code
**"This promo code is not valid"**
- **"View available offers"** link
- Suggestions for valid codes

#### Payment Failed
**"Payment could not be processed"**
- **"Try again"** with different method
- **"Contact support"** for assistance

#### Shipping Unavailable
**"Shipping not available to this location"**
- **"Check other PIN codes"** nearby
- **"Contact support"** for assistance

---

## 11. Analytics & Conversion Optimization

### A/B Testing Elements
- **CTA button colors** and text
- **Trust badge placement**
- **Checkout flow** steps
- **Payment method** order

### Conversion Optimization
- **Guest checkout** as default
- **Auto-save** form data
- **Express checkout** options
- **Social proof** elements

### Abandonment Recovery
- **Exit intent** detection
- **Time-based** reminders
- **Email sequences** for abandoned carts
- **Retargeting** campaigns
