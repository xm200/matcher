rule strcat_rule_b {
    meta:
        name = "strcat"
    strings:
        $s = "strcat"
    condition:
        $s
}