<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
 <!--  <xsl:template match="/R/data/inf">
    <h3><xsl:value-of select="@name"/></h3>
    <br/>
    <br/>
    <xsl:copy-of select="."><xsl:apply-templates name="copy"/></xsl:copy-of>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
  -->
  <xsl:template match="/">
    <h1><xsl:value-of select="/R/data/inf/@name"/></h1>
    <xsl:element name="iframe">
      <xsl:attribute name="src">
        <xsl:text>/pages/</xsl:text><xsl:value-of select="/R/data/inf"/><xsl:text>.html</xsl:text>
      </xsl:attribute>
      <xsl:attribute name="frameborder">
        <xsl:text>no</xsl:text>
      </xsl:attribute>
      <xsl:attribute name="width">
        <xsl:text>700px</xsl:text>
      </xsl:attribute>
      <xsl:attribute name="height">
        <xsl:text>3500px</xsl:text>
      </xsl:attribute>
      <xsl:attribute name="scrolling">
        <xsl:text>auto</xsl:text>
      </xsl:attribute>
      <xsl:attribute name="align">
        <xsl:text>left</xsl:text>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>
