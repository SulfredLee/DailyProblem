/*
 * adopted from http://xmlsoft.org/tutorial/apg.html
 */

#include <string>
#include <list>
#include <fstream>
#include <algorithm>
#include <sstream>

#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

//Helper Functions for B64 decode
static const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/";

static inline bool is_base64(unsigned char c)
{
    return (isalnum(c) || (c == '+') || (c == '/'));
}

// base64 decoder
void base64_decode(const std::string& encoded_string, unsigned char** decoded_bytes, unsigned int* out_len)
{
    size_t in_len = encoded_string.size();
    size_t i = 0;
    size_t j = 0;
    int in_ = 0;
    unsigned char char_array_4[4], char_array_3[3];
    std::list<unsigned char> ret;

    while (in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
        char_array_4[i++] = encoded_string[in_]; in_++;
        if (i ==4) {
            for (i = 0; i <4; i++)
                char_array_4[i] = static_cast<unsigned char>(base64_chars.find(char_array_4[i]));

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (i = 0; (i < 3); i++)
                ret.push_back(char_array_3[i]);
            i = 0;
        }
    }

    if (i) {
        for (j = i; j <4; j++)
            char_array_4[j] = 0;

        for (j = 0; j <4; j++)
            char_array_4[j] = static_cast<unsigned char>(base64_chars.find(char_array_4[j]));

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for (j = 0; (j < i - 1); j++) ret.push_back(char_array_3[j]);
    }

    *out_len = ret.size();
    *decoded_bytes = (unsigned char*) malloc(*out_len);
    for (i = 0; !ret.empty(); ++i, ret.pop_front())
    {
        (*decoded_bytes)[i] = ret.front();
    }
}

std::string base64_encode(unsigned char const* bytes_to_encode, unsigned int in_len) {
  std::string ret;
  int i = 0;
  int j = 0;
  unsigned char char_array_3[3];
  unsigned char char_array_4[4];

  while (in_len--) {
    char_array_3[i++] = *(bytes_to_encode++);
    if (i == 3) {
      char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
      char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
      char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
      char_array_4[3] = char_array_3[2] & 0x3f;

      for(i = 0; (i <4) ; i++)
        ret += base64_chars[char_array_4[i]];
      i = 0;
    }
  }

  if (i)
  {
    for(j = i; j < 3; j++)
      char_array_3[j] = '\0';

    char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
    char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
    char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
    char_array_4[3] = char_array_3[2] & 0x3f;

    for (j = 0; (j < i + 1); j++)
      ret += base64_chars[char_array_4[j]];

    while((i++ < 3))
      ret += '=';

  }

  return ret;

}

static void GetMsec(unsigned long long& outMsec, char* uri)
{
    unsigned long long hour, min, sec, msec;
    sscanf(uri, "%llu:%llu:%llu.%llu", &hour, &min, &sec, &msec);
    outMsec = (hour * 3600 + min * 60 + sec) * 1000 + msec;

    printf("hour: %llu min: %llu sec: %llu msec: %llu\n", hour, min, sec, msec);
    printf("outMsec: %llu\n", outMsec);
}
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
                // printf("node type: Text, content: %s\n", cur_node->children->content);
                std::string content((char*)cur_node->children->content);
                content.erase(std::remove_if(content.begin(), content.end(), isspace), content.end());
                unsigned char* decodedContent = NULL;
                unsigned int len = 0;
                base64_decode(content, &decodedContent, &len);
                printf("content.size(): %lu len: %d\n", content.size(), len);

                std::ofstream FH;
                FH.open("image.png", std::ios::binary | std::ios::out);
                FH.write((char*)decodedContent, len);
                FH.close();

                unsigned int width, height;
                memcpy((char*)&width, decodedContent + 16, sizeof(unsigned int));
                memcpy((char*)&height, decodedContent + 20, sizeof(unsigned int));

                width = ntohl(width);
                height = ntohl(height);
                printf("width: %u, height: %u\n", width, height);
            }
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"encoding");
            printf("uri: %s\n", uri == NULL ? "NULLLLLL" : (char*)uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"imagetype");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"id");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }
        else if (cur_node->type == XML_ELEMENT_NODE && xmlStrcmp(cur_node->name, (xmlChar *)"tt") == 0)
        {
            printf("node type: Element, name: %s\n", cur_node->name);
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"extent");
            printf("uri: %s\n", uri);
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
            std::string temp((char*)uri);
            temp.erase(std::remove(temp.begin(), temp.end(), '%'), temp.end());
            int extent_x, extent_y;
            sscanf(temp.c_str(), "%d %d", &extent_x, &extent_y);
            printf("extent_x: %d extent_y: %d\n", extent_x, extent_y);
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
            unsigned long long beginMsec;
            GetMsec(beginMsec, (char*)uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"end");
            printf("uri: %s\n", uri);
            unsigned long long endMsec;
            GetMsec(endMsec, (char*)uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"region");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"backgroundImage");
            printf("uri: %s\n", uri);
            xmlFree(uri);
        }
        else if (cur_node->type == XML_ELEMENT_NODE && xmlStrcmp(cur_node->name, (xmlChar *)"p") == 0)
        {
            printf("node type: Element, name: %s\n", cur_node->name);
            xmlChar* uri;
            uri = xmlGetProp(cur_node, (xmlChar*)"begin");
            printf("uri: %s\n", uri);
            unsigned long long beginMsec;
            GetMsec(beginMsec, (char*)uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"end");
            printf("uri: %s\n", uri);
            unsigned long long endMsec;
            GetMsec(endMsec, (char*)uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"region");
            printf("uri: %s\n", uri);
            xmlFree(uri);
            uri = xmlGetProp(cur_node, (xmlChar*)"backgroundImage");
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
        return 0;
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
    return 0;
}
