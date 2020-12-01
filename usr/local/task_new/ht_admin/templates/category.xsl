<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/category'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category?category_id=<xsl:value-of select='@category_id'/>&#38;parent_category=<xsl:value-of select='@category_id'/>&#38;parent_cat=<xsl:value-of select='@category_id'/></xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@discription'/></td>
          <td><xsl:value-of select='@warning'/></td>
          <td width='200px'>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category_link?category_id=<xsl:value-of select='@category_id'/></xsl:attribute>
              <xsl:text>доп. ссылки</xsl:text>  
            </xsl:element>
            <br/> 
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category?action=delete&#38;category_id=<xsl:value-of select='@category_id'/>&#38;parent_category=<xsl:value-of select='/R/data/@parent_category'/></xsl:attribute>
              удалить
            </xsl:element>
            <br/> 
            <xsl:element name='a'>
              <xsl:attribute name='href'>./category?action=delete_prod&#38;category_id=<xsl:value-of select='@category_id'/>&#38;parent_category=<xsl:value-of select='/R/data/@parent_category'/></xsl:attribute>
              удалить продукты
            </xsl:element>
            <br/> 
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./category?action=&#38;parent_category=<xsl:value-of select='/R/data/@parent_category'/>&#38;parent_cat=<xsl:value-of select='/R/data/@parent_category'/></xsl:attribute>
     Добавить категорию
    </xsl:element>
    <xsl:element name='a'>
      <xsl:attribute name='href'>./category?action=&#38;category_id=<xsl:value-of select='/R/data/@parent_cat'/>&#38;parent_category=<xsl:value-of select='/R/data/@parent_cat'/></xsl:attribute>
      На уровень вверх
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>

