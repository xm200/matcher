rule memcpy_rule_bin {
    strings:
        $s1 = "memcpy"
    condition:
        $s1
}