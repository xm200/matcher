rule memcpy_rule {
    meta:
        name = "memcpy"
    strings:
        $s1 = "memcpy("
    condition:
        $s1
}
