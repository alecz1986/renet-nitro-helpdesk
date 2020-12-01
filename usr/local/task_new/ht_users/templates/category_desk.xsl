<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <a href='/' css:color="#C50069" css:font-weight="bold" css:font-size="15px" css:BORDER-BOTTOM="1px dashed #C50069">Интернет-магазин "Пешка"</a>
    <xsl:for-each select="/R/data/categorys/category">
      <xsl:text> > </xsl:text>
      <xsl:element name='a'>
        <xsl:attribute name='href'>/<xsl:value-of select="@template"/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
        <xsl:attribute name='css:font-size'>15px</xsl:attribute>
        <xsl:attribute name='css:BORDER-BOTTOM'>1px dashed #C50069</xsl:attribute>
        <xsl:value-of select="@name"/>
      </xsl:element>
    </xsl:for-each>
    <br/>
    <br/>
    <div class='week-goods goods' css:width="760px;">
      <xsl:for-each select="/R/data/products/product">
        <p class="center-column-goods" css:width='247px' css:height="250px">
        <b css:padding="0px" css:margin="3px 0px">
          <xsl:element name='a'>
            <xsl:attribute name='href'>/product?product_id=<xsl:value-of select='@id'/></xsl:attribute>
            <xsl:value-of select='@name'/>
          </xsl:element>
        </b>
        <em css:font-size="9px" css:margin="10px 0px" css:padding='5px 0px' css:height="40px" width="230px">
          <xsl:value-of select="."/>
        </em>
              <xsl:element name='a'>
                <xsl:attribute name="width">250px</xsl:attribute>
                <xsl:attribute name="height">110px</xsl:attribute>
                <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="./photo/@path"/>/<xsl:value-of select="./photo/@name"/>.png</xsl:attribute>
               <xsl:attribute name='onclick'>return hs.expand(this,
                          {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})</xsl:attribute>
                <xsl:element name="img">
                  <xsl:attribute name="src">
                    <xsl:value-of select='/R/page/serv/@name'/>
                    <xsl:value-of select='./photo/@path'/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="./photo/@name"/>
                    <xsl:text>_small.png</xsl:text>
                  </xsl:attribute>
                  <xsl:if test="./photo/@small_x != 'None'">
                    <xsl:attribute name="width"><xsl:value-of select='./photo/@small_x'/></xsl:attribute>
                    <xsl:attribute name="height"><xsl:value-of select='./photo/@small_y'/></xsl:attribute>
                  </xsl:if>  
                  <xsl:attribute name="border">0</xsl:attribute>
                  <xsl:attribute name="css:margin">5px 50px</xsl:attribute>
                  <xsl:attribute name="align">center</xsl:attribute>
                </xsl:element>
            </xsl:element>
        <span class='price' css:margin-left="10px"><xsl:value-of select='@price'/></span>
        <span>
          <xsl:element name='a'>
            <xsl:attribute name="href">add2cart?product_id=<xsl:value-of select='@id'/>&#38;path_info=<xsl:value-of select='/R/page/path_encode'/></xsl:attribute>
            <xsl:attribute name="class">buy</xsl:attribute>
            <!--            <xsl:attribute name="css:color">#C50069</xsl:attribute>-->
            <xsl:attribute name="css:margin-left">105px</xsl:attribute>
            <xsl:text>заказать</xsl:text>
          </xsl:element>
        </span></p>
      </xsl:for-each>
      <br css:float="none" css:clear="both"/>
      <br/>
      <div css:margin="3px 0px"><h4>Страницы</h4></div>
    <xsl:value-of select='/R/data/pages/prev/@val'/>
    <xsl:for-each select="/R/data/pages/page">
      <xsl:choose>
        <xsl:when test='@action = "1"'>
          <b><xsl:value-of select='@val'/></b>
          <xsl:text>&#160;  &#160;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:element name="a">
            <xsl:attribute name="href">/order_desk?category_id=<xsl:value-of select='@id'/>&#38;page=<xsl:value-of select='@val'/>&#38;price=<xsl:value-of select='/R/data/@price'/></xsl:attribute>
            <xsl:value-of select='@val'/>
          </xsl:element>  
          <xsl:text>&#160;  &#160;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:value-of select='/R/data/pages/next/@val'/>
    </div>
  </xsl:template>
  <xsl:template name="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
