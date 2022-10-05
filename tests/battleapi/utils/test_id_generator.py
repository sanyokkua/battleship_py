import battleapi.utils.id_generator as id_gen


class TestUuid4IdGenerator:
    def test_id_generation(self) -> None:
        generator = id_gen.Uuid4IdGenerator()

        val_1 = generator.generate_id()
        assert val_1 is not None
        assert len(val_1) > 0

        set_of_ids = set()
        for _ in range(1000):
            set_of_ids.add(generator.generate_id())
        assert len(set_of_ids) == 1000
