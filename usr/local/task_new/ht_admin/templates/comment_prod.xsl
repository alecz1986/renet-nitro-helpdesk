<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/comment'>
        <tr>
          <td><xsl:value-of select='@name'/></td>
          <td>
            <xsl:element name='font'>
              <xsl:attribute name='css:color'><xsl:if test='@status="yes"'>green</xsl:if><xsl:if test='@status="no"'>red</xsl:if></xsl:attribute>
              <xsl:value-of select='@comment'/>
            </xsl:element>
          </td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>/product?product_id=<xsl:value-of select='@prod_id'/></xsl:attribute>
              <xsl:attribute name='target'>_blank</xsl:attribute>
              <xsl:value-of select='@prod_name'/> 
            </xsl:element>
          </td>
          <td width='200px'>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./comment?action=delete&#38;comment_id=<xsl:value-of select='@comment_id'/></xsl:attribute>
              удалить
            </xsl:element>
            <br/> 
            <xsl:element name='a'>
              <xsl:attribute name='href'>./comment?comment_id=<xsl:value-of select='@comment_id'/></xsl:attribute>
              редактировать 
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./comment</xsl:attribute>
     Добавить категорию
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

