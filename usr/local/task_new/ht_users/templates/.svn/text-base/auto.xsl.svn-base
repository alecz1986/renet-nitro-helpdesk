<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br css:clear="both"/>
    <a href='/' css:color="#C50069" css:font-weight="bold" css:font-size="15px" css:BORDER-BOTTOM="1px dashed #C50069" css:float="none">Интернет-магазин "Пешка"</a>
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
    <font css:font-size='12px' css:font-family='Arial,Verdana,Tahoma,sans-serif' css:margin='15px'><xsl:copy-of select="/R/data/discription/*"><xsl:apply-templates name="copy"/></xsl:copy-of></font>
    <br/>
    <div class='week-goods goods' css:clear="borth"  align="center">
      <xsl:for-each select="/R/data/childs/category">
        <p class="center-column-goods" css:width='242px' css:padding="1px" css:height="200px">
          <xsl:element name="a">
            <xsl:attribute name="href">/<xsl:value-of select="@template"/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="align">left</xsl:attribute>
            <xsl:attribute name="title"><xsl:value-of select="@name"/></xsl:attribute>
            <font size='2' css:margin-left="0px"><xsl:value-of select="@name"/></font>
            <xsl:element name="img">
              <xsl:attribute name="src">/category/<xsl:value-of select="@photo"/></xsl:attribute>
              <xsl:attribute name="width">160px</xsl:attribute>
              <xsl:attribute name="align">center</xsl:attribute>
              <xsl:attribute name="css:border">0px</xsl:attribute>
              <xsl:attribute name="css:margin-top">2px</xsl:attribute>
              <xsl:attribute name="css:padding">2px 30px</xsl:attribute>

            </xsl:element>
          </xsl:element>
        </p>
      </xsl:for-each>
    </div>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>                                                                                                                                          
