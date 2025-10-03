import React, { useEffect } from 'react';

const AdSenseAd = ({ 
  adSlot, 
  adFormat = 'auto', 
  adLayout = null,
  adLayoutKey = null,
  className = '',
  style = {},
  fullWidthResponsive = true 
}) => {
  const clientId = process.env.REACT_APP_ADSENSE_CLIENT_ID;

  useEffect(() => {
    try {
      if (window.adsbygoogle && window.adsbygoogle.loaded) {
        window.adsbygoogle.push({});
      }
    } catch (error) {
      console.error('AdSense error:', error);
    }
  }, []);

  const adStyle = {
    display: 'block',
    ...style
  };

  return (
    <div className={`adsense-container ${className}`}>
      <ins
        className="adsbygoogle"
        style={adStyle}
        data-ad-client={clientId}
        data-ad-slot={adSlot}
        data-ad-format={adFormat}
        data-ad-layout={adLayout}
        data-ad-layout-key={adLayoutKey}
        data-full-width-responsive={fullWidthResponsive}
      />
    </div>
  );
};

export default AdSenseAd;