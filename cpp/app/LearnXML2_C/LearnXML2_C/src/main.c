/*
 * adopted from http://xmlsoft.org/tutorial/apg.html
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

/**
 * print_element_names:
 * @a_node: the initial xml node to consider.
 *
 * Prints the names of the all the xml elements
 * that are siblings or children of a given xml node.
 */
static void print_element_names(xmlNodePtr a_node)
{
    xmlNodePtr cur_node = NULL;

    for (cur_node = a_node; cur_node; cur_node = cur_node->next)
    {
        if (cur_node->type == XML_ELEMENT_NODE && xmlStrcmp(cur_node->name, (xmlChar *)"image") == 0)
        {
            printf("node type: Element, name: %s\n", cur_node->name);
            if (cur_node->children)
            {
                printf("node type: Text, content: %s\n", cur_node->children->content);
            }
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"encodin");
            printf("uri: %s\n", uri == NULL ? "NULLLLLL" : "Has");
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"imagetype");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"id");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }
        else if (cur_node->type == XML_ELEMENT_NODE && xmlStrcmp(cur_node->name, (xmlChar *)"region") == 0)
        {
            printf("node type: Element, name: %s\n", cur_node->name);
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"id");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"extent");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"origin");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }
        else if (cur_node->type == XML_ELEMENT_NODE && xmlStrcmp(cur_node->name, (xmlChar *)"div") == 0)
        {
            printf("node type: Element, name: %s\n", cur_node->name);
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"begin");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"end");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"region");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"backgroundImage");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"id");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }

        print_element_names(cur_node->children);
    }
}

int main(int argc, char **argv)
{

    char         *docname;
    xmlDocPtr    doc;
    xmlNodePtr   cur;
    xmlChar      *uri;

    if (argc <= 1)
    {
        printf("Usage: %s docname\n", argv[0]);
        return(0);
    }

    docname = argv[1];

    doc = xmlParseFile(docname);
    cur = xmlDocGetRootElement(doc);
    print_element_names(cur);
    xmlFreeDoc(doc);
    return 1;

    cur = cur->xmlChildrenNode;
    while (cur != NULL)
    {
        if ((!xmlStrcmp(cur->name, (const xmlChar *)"reference")))
        {
            uri = xmlGetProp(cur, (xmlChar *)"uri");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }
        cur = cur->next;
    }
    xmlFreeDoc(doc);
    return (1);
}
