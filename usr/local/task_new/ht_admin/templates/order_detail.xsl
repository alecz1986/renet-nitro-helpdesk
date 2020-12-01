<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <xsl:element name='input'>
      <xsl:attribute name='type'>hidden</xsl:attribute>
      <xsl:attribute name='id'>se.order_id</xsl:attribute>
      <xsl:attribute name='value'><xsl:value-of select='/R/data/@order_id'/></xsl:attribute>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

