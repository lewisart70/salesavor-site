import React from 'react';
import { Button } from './ui/button';
import { ArrowLeft } from 'lucide-react';

const TermsOfService = ({ onBack }) => {
  return (
    <div className="min-h-screen" style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', backgroundColor: '#f5f5f5' }}>
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4">
            <Button 
              onClick={onBack}
              variant="outline"
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
            <div className="flex items-center gap-3">
              <img 
                src={process.env.REACT_APP_LOGO_URL} 
                alt="SaleSavor App Icon" 
                className="h-8 w-8 rounded-lg"
              />
              <span className="text-xl font-bold" style={{ color: '#2c5f2d' }}>
                SaleSavor
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Terms of Service Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <style dangerouslySetInnerHTML={{
            __html: `
              [data-custom-class='body'], [data-custom-class='body'] * {
                background: transparent !important;
              }
              [data-custom-class='title'], [data-custom-class='title'] * {
                font-family: Arial !important;
                font-size: 26px !important;
                color: #000000 !important;
              }
              [data-custom-class='subtitle'], [data-custom-class='subtitle'] * {
                font-family: Arial !important;
                color: #595959 !important;
                font-size: 14px !important;
              }
              [data-custom-class='heading_1'], [data-custom-class='heading_1'] * {
                font-family: Arial !important;
                font-size: 19px !important;
                color: #000000 !important;
              }
              [data-custom-class='heading_2'], [data-custom-class='heading_2'] * {
                font-family: Arial !important;
                font-size: 17px !important;
                color: #000000 !important;
              }
              [data-custom-class='body_text'], [data-custom-class='body_text'] * {
                color: #595959 !important;
                font-size: 14px !important;
                font-family: Arial !important;
              }
              [data-custom-class='link'], [data-custom-class='link'] * {
                color: #3030F1 !important;
                font-size: 14px !important;
                font-family: Arial !important;
                word-break: break-word !important;
              }
              ul {
                list-style-type: square;
              }
              ul > li > ul {
                list-style-type: circle;
              }
              ul > li > ul > li > ul {
                list-style-type: square;
              }
              ol li {
                font-family: Arial;
              }
              .MsoNormal {
                margin-bottom: 0.5rem;
              }
              h1, h2, h3 {
                margin-top: 1.5rem;
                margin-bottom: 1rem;
              }
            `
          }} />
          
          <div data-custom-class="body" dangerouslySetInnerHTML={{
            __html: `
              <div align="center" style="text-align: left;"><div class="MsoNormal" data-custom-class="title" style="line-height: 1.5;"><bdt class="block-component"><span style="font-size: 19px;"></bdt><bdt class="question"><strong><h1>TERMS OF SERVICE</h1></strong></bdt><bdt class="statement-end-if-in-editor"></bdt></span></div><div class="MsoNormal" data-custom-class="subtitle" style="line-height: 1.5;"><strong>Last updated</strong> <bdt class="question"><strong>November 27, 2025</strong></bdt></div><div class="MsoNormal" style="line-height: 1.1;"><br></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><strong><span data-custom-class="heading_1"><h2>AGREEMENT TO OUR LEGAL TERMS</h2></span></strong></div></div><div align="center" style="text-align: left;"><div class="MsoNormal" id="agreement" style="line-height: 1.5;"><a name="_6aa3gkhykvst"></a></div></div><div align="center" style="text-align: left;"><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">We are <bdt class="block-container question question-in-editor" data-id="9d459c4e-c548-e5cb-7729-a118548965d2" data-type="question noTranslate">SaleSavor</bdt><bdt class="block-component"></bdt> (<bdt class="block-component"></bdt>'<strong>Company</strong>', '<strong>we</strong>', '<strong>us</strong>', or '<strong>our</strong>'<bdt class="else-block"></bdt>), a company registered in <bdt class="question noTranslate">Canada</bdt> at <bdt class="question noTranslate">38 Faircrest Blvd</bdt>, <bdt class="question noTranslate">Kingston</bdt>, <bdt class="question noTranslate">Ontario</bdt> <bdt class="question noTranslate">K7L 4V1</bdt>.</span></div></div>
              
              <div align="center" style="text-align: left;"><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">We operate <bdt class="block-component"></bdt>the website <span style="color: rgb(0, 58, 250);"><bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="http://salesavor.ca">http://salesavor.ca</a></bdt></span> (the <bdt class="block-component"></bdt>'<strong>Site</strong>'<bdt class="else-block"></bdt>), the mobile application <bdt class="question noTranslate">SaleSavor</bdt> (the <bdt class="block-component"></bdt>'<strong>App</strong>'<bdt class="else-block"></bdt>), as well as any other related products and services that refer or link to these legal terms (the <bdt class="block-component"></bdt>'<strong>Legal Terms</strong>'<bdt class="else-block"></bdt>) (collectively, the <bdt class="block-component"></bdt>'<strong>Services</strong>'<bdt class="else-block"></bdt>).</span></div>
              
              <div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><bdt class="question">SaleSavor is a grocery planning and money-saving tool that helps Canadian families discover weekly grocery sales, get personalized recipe recommendations based on dietary needs, and create smart shopping lists. The service is available via mobile app and website, with optional account creation for saving preferences and lists.</bdt></div>
              
              <div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">You can contact us by <bdt class="block-component"></bdt>phone at <bdt class="question">1-613-246-5411</bdt>, email at <bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="mailto:info@salesavor.ca">info@salesavor.ca</a></bdt>, or by mail to <bdt class="question noTranslate">38 Faircrest Blvd</bdt>, <bdt class="question noTranslate">Kingston</bdt>, <bdt class="question noTranslate">Ontario</bdt> <bdt class="question noTranslate">K7L 4V1</bdt>, <bdt class="question noTranslate">Canada</bdt>.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">These Legal Terms constitute a legally binding agreement made between you, whether personally or on behalf of an entity ('you'), and <bdt class="question noTranslate">SaleSavor</bdt>, concerning your access to and use of the Services. You agree that by accessing the Services, you have read, understood, and agreed to be bound by all of these Legal Terms. IF YOU DO NOT AGREE WITH ALL OF THESE LEGAL TERMS, THEN YOU ARE EXPRESSLY PROHIBITED FROM USING THE SERVICES AND YOU MUST DISCONTINUE USE IMMEDIATELY.</span></div>

              <div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">We will provide you with prior notice of any scheduled changes to the Services you are using. Changes to these Legal Terms will become effective <bdt class="question">thirty (30)</bdt> days after the notice is given, except if the changes apply to <bdt class="question">security updates</bdt>, <bdt class="question">bug fixes</bdt>, and <bdt class="question">a court order</bdt>, in which case the changes will be effective immediately. By continuing to use the Services after the effective date of any changes, you agree to be bound by the modified terms.</span></div>

              <div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;">The Services are intended for users who are at least 18 years old. Persons under the age of 18 are not permitted to use or register for the Services.</div><div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5;">We recommend that you print a copy of these Legal Terms for your records.</div>

              <div class="MsoNormal" data-custom-class="heading_1" style="line-height: 1.5;"><strong><h2>TABLE OF CONTENTS</h2></strong></div><div class="MsoNormal" style="line-height: 1.5;"><a data-custom-class="link" href="#services"><span data-custom-class="link"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text">1. OUR SERVICES</span></span></span></a></div><div class="MsoNormal" style="line-height: 1.5;"><a data-custom-class="link" href="#ip"><span style="color: rgb(0, 58, 250);"><span data-custom-class="body_text">2. INTELLECTUAL PROPERTY RIGHTS</span></span></a></div><div class="MsoNormal" style="line-height: 1.5;"><a data-custom-class="link" href="#userreps"><span style="color: rbg(0, 58, 250); font-size: 15px; line-height: 1.5;"><span data-custom-class="body_text">3. USER REPRESENTATIONS</span></span></a></div>

              <div class="MsoNormal" style="line-height: 1.5;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="addclause" style="line-height: 1.5; text-align: left;"><span style="font-size: 19px;"><strong><h2>25. NO MEDICAL OR NUTRITIONAL ADVICE</h2></strong></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;">The information provided through the Services, including recipe recommendations and dietary filtering, is for informational purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment. We are not healthcare providers, nutritionists, or dietitians. Always seek the advice of your physician or other qualified health provider regarding medical conditions or dietary needs. Never disregard professional medical advice because of something accessed through the Services.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="addclauseb" style="line-height: 1.5; text-align: left;"><span style="font-size: 19px;"><h2>26. RECIPE ACCURACY AND FOOD SAFETY</h2></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;">Recipes provided through the Services are sourced from third parties. We make no representations about the accuracy, completeness, nutritional information, or presence of allergens in recipes. Users are solely responsible for verifying ingredient lists, following safe food handling practices, and ensuring proper cooking methods. We are not liable for any illness, injury, or adverse reaction resulting from the preparation or consumption of any recipe.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="addclausec" style="line-height: 1.5; text-align: left;"><span style="font-size: 19px;"><h2>27. AI-GENERATED CONTENT</h2></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;">Certain features use artificial intelligence to provide personalized recommendations. AI-generated content may not always be accurate or suitable for your needs. We make no guarantees regarding the accuracy or suitability of AI recommendations. You are responsible for reviewing and verifying recommendations before relying on them and using your own judgment regarding diet and health decisions.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="addclaused" style="line-height: 1.5; text-align: left;"><span style="font-size: 19px;"><h2>28. THIRD-PARTY CONTENT AND SERVICES</h2></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;">The Services integrate with third-party providers including recipe databases and grocery information. We do not control or endorse third-party content and are not responsible for its accuracy, quality, or availability. Third-party pricing and product information may change without notice. Your interactions with third parties are governed by their own terms and privacy policies.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="addclausee" style="line-height: 1.5; text-align: left;"><span style="font-size: 19px;"><h2>29. AFFILIATE RELATIONSHIPS</h2></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;">The Services may include affiliate links from which we earn commissions. These relationships do not affect prices you pay. When you use affiliate links, you are redirected to third-party sites subject to their terms. We are not responsible for products, services, fulfillment, or disputes with third-party vendors. Commission relationships do not influence our recommendations.</span></div>
              
              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="heading_1" id="contact" style="line-height: 1.5; text-align: left;"><strong><span style="line-height: 115%; font-family: Arial;"><span style="font-size: 19px; line-height: 1.5;"><h2>30. CONTACT US</h2></span></span></strong></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;">In order to resolve a complaint regarding the Services or to receive further information regarding use of the Services, please contact us at:</span></div><div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><bdt class="question noTranslate"><strong>SaleSavor</strong></bdt></span></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;"><span style="line-height: 115%; font-family: Arial; color: rgb(89, 89, 89);"><bdt class="question"><strong><bdt class="question noTranslate">38 Faircrest Blvd</bdt></strong></bdt></span></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><span style="font-size: 15px;"><strong><span style="color: rgb(89, 89, 89);"><bdt class="question"><bdt class="question noTranslate">Kingston, Ontario K7L 4V1</bdt></bdt></span></strong></span></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><bdt class="question noTranslate"><strong>Canada</strong></bdt></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><strong><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;"><strong>Phone: <bdt class="question">1-613-246-5411</bdt></strong></span></strong></div><div class="MsoNormal" data-custom-class="body_text" style="line-height: 1.5; text-align: left;"><strong><span style="font-size:11.0pt;line-height:115%;font-family:Arial;
Calibri;color:#595959;mso-themecolor:text1;mso-themetint:166;"><strong><bdt class="question"><bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="mailto:info@salesavor.ca">info@salesavor.ca</a></bdt></bdt></strong></span></strong></div>

              <div class="MsoNormal" style="line-height: 1.5; text-align: left;"><br></div>
              <div style="background: #f0f8ff; border: 1px solid #d0e8ff; border-radius: 8px; padding: 16px; margin: 24px 0;">
                <h3 style="color: #2c5f2d; margin-bottom: 12px; font-size: 18px;">Important Disclaimers for SaleSavor Users</h3>
                <div style="margin-bottom: 16px;">
                  <h4 style="color: #1a1a1a; margin-bottom: 8px; font-size: 16px;">🏥 No Medical Advice</h4>
                  <p style="color: #595959; font-size: 14px; margin-bottom: 0;">Recipe suggestions and dietary filters are for informational purposes only. Always consult healthcare professionals for medical or dietary advice.</p>
                </div>
                <div style="margin-bottom: 16px;">
                  <h4 style="color: #1a1a1a; margin-bottom: 8px; font-size: 16px;">🍳 Recipe & Food Safety</h4>
                  <p style="color: #595959; font-size: 14px; margin-bottom: 0;">You are responsible for verifying ingredients, allergens, and following safe food handling practices. We are not liable for any food-related issues.</p>
                </div>
                <div style="margin-bottom: 16px;">
                  <h4 style="color: #1a1a1a; margin-bottom: 8px; font-size: 16px;">🤖 AI-Generated Content</h4>
                  <p style="color: #595959; font-size: 14px; margin-bottom: 0;">AI recommendations may not always be accurate. Use your own judgment and verify recommendations before relying on them.</p>
                </div>
                <div>
                  <h4 style="color: #1a1a1a; margin-bottom: 8px; font-size: 16px;">💰 Price Verification</h4>
                  <p style="color: #595959; font-size: 14px; margin-bottom: 0;">Always verify pricing, availability, and promotional terms at stores before shopping. We are not responsible for price changes or store policy differences.</p>
                </div>
              </div>
            `
          }} />
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;