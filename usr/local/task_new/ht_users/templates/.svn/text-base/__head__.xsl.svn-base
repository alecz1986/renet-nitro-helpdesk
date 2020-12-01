<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title><xsl:value-of select="/R/page/title"/></title>
    <xsl:element name='link'>
      <xsl:attribute name='rel'>stylesheet</xsl:attribute>
      <xsl:attribute name='type'>text/css</xsl:attribute>
      <xsl:attribute name='href'>/css/<xsl:value-of select='/R/page/@css'/></xsl:attribute>
    </xsl:element>
    <link rel="stylesheet" type="text/css" href="/data/highslide/highslide.css" />
    <script type="text/javascript" src="/data/highslide/highslide.js"></script>
    <script type="text/javascript" src="/js/swf.js"></script>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <script type="text/javascript" src="/js/height.js"></script>
    <script type="text/javascript" src="/data/html_tag.js"></script>
    <script type="text/javascript" src="/data/star.js"></script>
    <xsl:choose>
      <xsl:when test="/R/data/kws">
        <xsl:element name="META">
          <xsl:attribute name="name">keywords</xsl:attribute>
          <xsl:attribute name="content">
            <xsl:value-of select="/R/data/kws/@kw"/>
          </xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="META">
          <xsl:attribute name="name">keywords</xsl:attribute>
          <xsl:attribute name="content">
            <xsl:text>интернет-магазин пешка, саратов,первый в саратове интернет-магазин необходимых вещей саратов</xsl:text>
          </xsl:attribute>
        </xsl:element>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:element name="META">
      <xsl:attribute name="name">description</xsl:attribute>
      <xsl:attribute name="content"><xsl:value-of select="/R/page/title"/></xsl:attribute>
    </xsl:element>
    <meta name="google-site-verification" content="kXaKKJNVSQn6wTPkZOLiWL2oLPE2s4kiljmy9B47a8E" />
    <meta name='yandex-verification' content='' />
    <link rel="icon" href="http://peshca.ru/favicon.ico" type="image/x-icon" sizes='16x16'/>
    <link rel="shortcut icon" href="http://peshca.ru/favicon.ico" type="image/x-icon"/> 
  </xsl:template>
</xsl:stylesheet>
