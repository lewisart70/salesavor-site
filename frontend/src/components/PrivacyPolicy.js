import React from 'react';
import { Button } from './ui/button';
import { ArrowLeft } from 'lucide-react';

const PrivacyPolicy = ({ onBack }) => {
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

      {/* Privacy Policy Content */}
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
              table {
                border-collapse: collapse;
                width: 100%;
                margin: 1rem 0;
              }
              th, td {
                border: 1px solid #000;
                padding: 8px;
                text-align: left;
              }
              th {
                background-color: #f5f5f5;
                font-weight: bold;
              }
            `
          }} />
          
          <div data-custom-class="body" dangerouslySetInnerHTML={{
            __html: `
              <div><strong><span style="font-size: 26px;"><span data-custom-class="title"><bdt class="block-component"></bdt><bdt class="question"><h1>PRIVACY POLICY</h1></bdt><bdt class="statement-end-if-in-editor"></bdt></span></span></strong></div><div><span style="color: rgb(127, 127, 127);"><strong><span style="font-size: 15px;"><span data-custom-class="subtitle">Last updated <bdt class="question">November 27, 2025</bdt></span></span></strong></span></div><div><br></div><div><br></div><div><br></div><div style="line-height: 1.5;"><span style="color: rgb(127, 127, 127);"><span style="color: rgb(89, 89, 89); font-size: 15px;"><span data-custom-class="body_text">This Privacy Notice for <bdt class="question noTranslate">SaleSavor</bdt><bdt class="block-component"></bdt></bdt> (<bdt class="block-component"></bdt>'<strong>we</strong>', '<strong>us</strong>', or '<strong>our</strong>'<bdt class="else-block"></bdt></span><span data-custom-class="body_text">), describes how and why we might access, collect, store, use, and/or share (<bdt class="block-component"></bdt>'<strong>process</strong>'<bdt class="else-block"></bdt>) your personal information when you use our services (<bdt class="block-component"></bdt>'<strong>Services</strong>'<bdt class="else-block"></bdt>), including when you:</span></span></span><span style="font-size: 15px;"><span style="color: rgb(127, 127, 127);"><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="block-component"></bdt></span></span></span></span></span></div><ul><li data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text">Visit our website<bdt class="block-component"></bdt> at <span style="color: rgb(0, 58, 250);"><bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="http://salesavor.ca">http://salesavor.ca</a></bdt></span><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><bdt class="statement-end-if-in-editor"> or any website of ours that links to this Privacy Notice</bdt></span></span></span></span></span></span></span></span></li></ul><div><bdt class="block-component"><span style="font-size: 15px;"><span style="font-size: 15px;"><span style="color: rgb(127, 127, 127);"><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="block-component"></bdt></span></span></span></span></span></span></bdt></div><ul><li data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text">Download and use<bdt class="block-component"></bdt> our mobile application<bdt class="block-component"></bdt> (<bdt class="question">SaleSavor)<span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><bdt class="statement-end-if-in-editor">,</bdt></span></span></span></span></span></span></span></span></bdt></span><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><bdt class="statement-end-if-in-editor"><bdt class="block-component"> or any other application of ours that links to this Privacy Notice</bdt></bdt></span></span></span></span></span></span></span></span></li></ul><div style="line-height: 1.5;"><bdt class="block-component"><span style="font-size: 15px;"></span></bdt></div><ul><li data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size: 15px;">Use <bdt class="question">SaleSavor</bdt>. <bdt class="question">SaleSavor is a mobile grocery planning application that helps families save money by aggregating weekly sales from local Canadian grocery stores, generating personalized recipe suggestions based on sale items and dietary preferences, and creating smart shopping lists. The app uses location services to find nearby stores, processes user dietary preferences and health concerns, and provides meal planning features to help users make the most of grocery sales and discounts.</bdt></span><bdt class="statement-end-if-in-editor"><span style="font-size: 15px;"></span></bdt></li></ul><div style="line-height: 1.5;"><span style="font-size: 15px;"><span style="color: rgb(127, 127, 127);"><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="block-component"></bdt></span></span></span></span></span></div><ul><li data-custom-class="body_text" style="line-height: 1.5;"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text">Engage with us in other related ways, including any marketing or events<span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><bdt class="statement-end-if-in-editor"></bdt></span></span></span></span></span></span></span></span></li></ul><div style="line-height: 1.5;"><span style="font-size: 15px;"><span style="color: rgb(127, 127, 127);"><span data-custom-class="body_text"><strong>Questions or concerns? </strong>Reading this Privacy Notice will help you understand your privacy rights and choices. We are responsible for making decisions about how your personal information is processed. If you do not agree with our policies and practices, please do not use our Services.<bdt class="block-component"></bdt> If you still have any questions or concerns, please contact us at <bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="mailto:info@salesavor.ca">info@salesavor.ca</a></bdt>.</span></span></span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><strong><span style="font-size: 15px;"><span data-custom-class="heading_1"><h2>SUMMARY OF KEY POINTS</h2></span></span></strong></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text"><strong><em>This summary provides key points from our Privacy Notice, but you can find out more details about any of these topics by clicking the link following each key point or by using our </em></strong></span></span><a data-custom-class="link" href="#toc"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text"><strong><em>table of contents</em></strong></span></span></a><span style="font-size: 15px;"><span data-custom-class="body_text"><strong><em> below to find the section you are looking for.</em></strong></span></span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text"><strong>What personal information do we process?</strong> When you visit, use, or navigate our Services, we may process personal information depending on how you interact with us and the Services, the choices you make, and the products and features you use. Learn more about </span></span><a data-custom-class="link" href="#personalinfo"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text">personal information you disclose to us</span></span></a><span data-custom-class="body_text">.</span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text"><strong>Do we process any sensitive personal information? </strong>Some of the information may be considered <bdt class="block-component"></bdt>'special' or 'sensitive'<bdt class="else-block"></bdt> in certain jurisdictions, for example your racial or ethnic origins, sexual orientation, and religious beliefs. <bdt class="block-component"></bdt>We may process sensitive personal information when necessary with your consent or as otherwise permitted by applicable law. Learn more about </span></span><a data-custom-class="link" href="#sensitiveinfo"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text">sensitive information we process</span></span></a><span data-custom-class="body_text">.</span><span style="font-size: 15px;"><span data-custom-class="body_text"><bdt class="statement-end-if-in-editor"></bdt></span></span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text"><strong>Do we collect any information from third parties?</strong> <bdt class="block-component"></bdt>We may collect information from public databases, marketing partners, social media platforms, and other outside sources. Learn more about </span></span><a data-custom-class="link" href="#othersources"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text">information collected from other sources</span></span></a><span data-custom-class="body_text">.</span><span style="font-size: 15px;"><span data-custom-class="body_text"><bdt class="statement-end-if-in-editor"></bdt></span></span></div>

              <div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text">Want to learn more about what we do with any information we collect? </span></span><a data-custom-class="link" href="#toc"><span style="color: rgb(0, 58, 250); font-size: 15px;"><span data-custom-class="body_text">Review the Privacy Notice in full</span></span></a><span style="font-size: 15px;"><span data-custom-class="body_text">.</span></span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><br></div><div id="toc" style="line-height: 1.5;"><span style="font-size: 15px;"><span style="color: rgb(127, 127, 127);"><span style="color: rgb(0, 0, 0);"><strong><span data-custom-class="heading_1"><h2>TABLE OF CONTENTS</h2></span></strong> </span> </span> </span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><a data-custom-class="link" href="#infocollect"><span style="color: rgb(0, 58, 250);">1. WHAT INFORMATION DO WE COLLECT?</span></a></span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><a data-custom-class="link" href="#infouse"><span style="color: rgb(0, 58, 250);">2. HOW DO WE PROCESS YOUR INFORMATION?<bdt class="block-component"></bdt></span></a></span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><a data-custom-class="link" href="#legalbases"><span style="color: rgb(0, 58, 250);">3. <span style="font-size: 15px;"><span style="color: rgb(0, 58, 250);">WHAT LEGAL BASES DO WE RELY ON TO PROCESS YOUR PERSONAL INFORMATION?</span></span><bdt class="statement-end-if-in-editor"></bdt></span></a></span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span style="color: rgb(0, 58, 250);"><a data-custom-class="link" href="#whoshare">4. WHEN AND WITH WHOM DO WE SHARE YOUR PERSONAL INFORMATION?</a></span><span data-custom-class="body_text"><bdt class="block-component"></bdt></a><span style="color: rgb(127, 127, 127);"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><bdt class="block-component"></bdt></span></span></span></span></span></div>

              <div style="line-height: 1.5;"><span style="font-size: 15px;"><a data-custom-class="link" href="#contact"><span style="color: rgb(0, 58, 250);">15. HOW CAN YOU CONTACT US ABOUT THIS NOTICE?</span></a></span></div><div style="line-height: 1.5;"><a data-custom-class="link" href="#request"><span style="color: rgb(0, 58, 250);">16. HOW CAN YOU REVIEW, UPDATE, OR DELETE THE DATA WE COLLECT FROM YOU?</span></a></div>

              <div id="contact" style="line-height: 1.5; margin-top: 2rem; padding-top: 2rem; border-top: 2px solid #e5e5e5;"><span style="color: rgb(127, 127, 127);"><span style="color: rgb(89, 89, 89); font-size: 15px;"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span id="control" style="color: rgb(0, 0, 0);"><strong><span data-custom-class="heading_1"><h2>15. HOW CAN YOU CONTACT US ABOUT THIS NOTICE?</h2></span></strong></span></span></span></span></span><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text">If you have questions or comments about this notice, you may <span style="color: rgb(89, 89, 89); font-size: 15px;"><span data-custom-class="body_text"><bdt class="block-component"></bdt></span></span>contact our Data Protection Officer (DPO)<span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text"> by email at </span></span></span><span style="color: rgb(89, 89, 89); font-size: 15px;"><span data-custom-class="body_text"><bdt class="question noTranslate"><a target="_blank" data-custom-class="link" href="mailto:info@salesavor.ca">info@salesavor.ca</a></bdt></span></span>,<bdt class="block-component"></bdt><bdt class="statement-end-if-in-editor"><span data-custom-class="body_text"></span></bdt><span style="color: rgb(89, 89, 89); font-size: 15px;"><span data-custom-class="body_text"><bdt class="else-block"><bdt class="block-component"></bdt> or <bdt class="statement-end-if-in-editor"></bdt></bdt></span></span><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text">contact us by post at:</span></span></span></span></span></span></div><div style="line-height: 1.5;"><br></div><div style="line-height: 1.5;"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span style="font-size: 15px; color: rgb(89, 89, 89);"><span data-custom-class="body_text"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="question noTranslate">SaleSavor</bdt></span></span></span></span></span><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="block-component"></bdt></span></span></span></span></span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span data-custom-class="body_text">Data Protection Officer</span><span style="color: rgb(89, 89, 89);"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="question"><span data-custom-class="body_text"><span style="color: rgb(89, 89, 89);"><bdt class="block-component"></bdt></span></span></bdt></span></span></span></span></div><div style="line-height: 1.5;"><span style="font-size: 15px;"><span style="color: rgb(89, 89, 89);"><span style="color: rgb(89, 89, 89);"><span data-custom-class="body_text"><bdt class="question noTranslate">38 Faircrest Blvd<br>Kingston, ON K7L 4V1<br>Canada</bdt></span></span></span></div>
            `
          }} />
        </div>
      </div>
    </div>
  );
};

export default PrivacyPolicy;