<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <font css:font-size='12px' css:font-family='Arial,Verdana,Tahoma,sans-serif' css:margin='15px'><xsl:copy-of select="/R/data/discription/*"><xsl:apply-templates name="copy"/></xsl:copy-of></font>
    <br/>
    <div class='week-goods goods' css:clear="borth"  align="center">
      <xsl:for-each select="/R/data/childs/category">
        <p class="center-column-goods" css:width='370px' css:padding="0px" css:height="200px" css:float='left'>
          <xsl:element name="a">
            <xsl:attribute name="href">/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="css:float">left</xsl:attribute>
            <xsl:attribute name="title"><xsl:value-of select="@name"/></xsl:attribute>
            <xsl:element name="img">
              <xsl:attribute name="src">/category/<xsl:value-of select="@photo"/></xsl:attribute>
              <xsl:attribute name="width">160px</xsl:attribute>
              <xsl:attribute name="align">center</xsl:attribute>
              <xsl:attribute name="css:border">0px</xsl:attribute>
              <xsl:attribute name="css:margin-top">2px</xsl:attribute>
              <xsl:attribute name="css:padding">2px 5px</xsl:attribute>
            </xsl:element>
          </xsl:element>
          <xsl:element name="a">
            <xsl:attribute name="href">/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
            <xsl:attribute name="align">left</xsl:attribute>
            <xsl:attribute name="css:float">left</xsl:attribute>
            <xsl:attribute name="css:text-align">left</xsl:attribute>
            <xsl:attribute name="css:width">190px</xsl:attribute>
            <xsl:attribute name="title"><xsl:value-of select="@name"/></xsl:attribute>
            <font css:font-size='15px' css:margin-left="0px" css:color="#C50069"><xsl:value-of select="@name"/></font>
          </xsl:element>
          <xsl:for-each select="./cat">
            <xsl:element name="a">
              <xsl:attribute name="href">/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
              <xsl:attribute name="class">food</xsl:attribute>
              <xsl:attribute name="title"><xsl:value-of select="@name"/></xsl:attribute>
              <font><xsl:value-of select="@name"/></font>
            </xsl:element>
          </xsl:for-each>
        </p>
      </xsl:for-each>
    </div>
  </xsl:template>
</xsl:stylesheet>                                                                                                                                          
