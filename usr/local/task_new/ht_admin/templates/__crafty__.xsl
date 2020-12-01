<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <xsl:copy-of select="/R/data/html/*" copy-namespace="yes"/>
  </xsl:template>
</xsl:stylesheet>
