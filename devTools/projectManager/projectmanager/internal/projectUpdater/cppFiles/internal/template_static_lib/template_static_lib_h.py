content_st = """
#ifndef {{ module_name }}_H
#define {{ module_name }}_H

/**
 * @brief {{ module_name }} class used for
 */
class {{ module_name }} {
public:
    /**
     * Create a new {{ module_name }} object
     * @brief Default constructor.
     * @see {{ module_name }}(param a, param b)
     * @see {{ module_name }}(param a, param b, param c)
     */
    {{ module_name }}();
    /**
     * Remove {{ module_name }} object
     * @brief Default destructor.
     */
    virtual ~{{ module_name }}();
    /**
     * @brief Get data from this object
     * @param Information from outside
     * @return The length of something
     */
    double GetLength(const double& xx);
};

#endif
"""
