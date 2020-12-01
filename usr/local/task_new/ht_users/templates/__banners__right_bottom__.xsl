<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
      <noindex>
        <script type='text/javascript'><xsl:comment><![CDATA[
           document.MAX_ct0 ='INSERT_CLICKURL_HERE';
           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=6");
           document.write ('&amp;cb=' + m3_r);
           if (document.MAX_used != ',') document.write ("&amp;exclude=" + document.MAX_used);
           document.write (document.charset ? '&amp;charset='+document.charset : (document.characterSet ? '&amp;charset='+document.characterSet : ''));
           document.write ("&amp;loc=" + escape(window.location));
           if (document.referrer) document.write ("&amp;referer=" + escape(document.referrer));
           if (document.context) document.write ("&context=" + escape(document.context));
           if ((typeof(document.MAX_ct0) != 'undefined') && (document.MAX_ct0.substring(0,4) == 'http')) {
           document.write ("&amp;ct0=" + escape(document.MAX_ct0));
           }
           if (document.mmm_fo) document.write ("&amp;mmm_fo=1");
           document.write ("'><\/scr"+"ipt>");
           //]]></xsl:comment></script><noscript><a href='http://abz.peshca.ru/www/delivery/ck.php?n=a7d9bd8a&amp;cb=INSERT_RANDOM_NUMBER_HERE' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=6&amp;cb=INSERT_RANDOM_NUMBER_HERE&amp;n=a7d9bd8a&amp;ct0=INSERT_CLICKURL_HERE' border='0' alt='' /></a></noscript>
     </noindex>
 </xsl:template>
</xsl:stylesheet>
